import re
from urllib.parse import urljoin
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

from common.services.scraping.parts.base import BasePartScraper, implements_platform_scraper, ScrapedPart
from common.database.models.car_model_platform import CarModelPlatform
from common.database.models.part_category import PartCategory


@implements_platform_scraper("ria")
class RiaPartScraper(BasePartScraper):
    async def __call__(self) -> list[ScrapedPart]:
        scraped_parts = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()
            
            try:
                # Navigate to the base URL
                await page.goto(self.platform_url, timeout=120000, wait_until="networkidle")

                await page.wait_for_timeout(1000)  # Wait for dynamic content to load
                
                category_found = await self._find_and_click_category(page)
                
                if category_found:
                    await page.wait_for_timeout(2000)
                    
                    scraped_parts = await self._extract_all_pages_parts_data(page)
                
            except Exception as e:
                print(f"Error scraping RIA website: {e}")
            finally:
                await browser.close()
        
        return scraped_parts
    
    async def _find_and_click_category(self, page) -> bool:
        """
        Find and click on the specified category
        """
        try:
            for category_name in self.category_names:
                try:
                    element = page.locator(f"a.catalog-rubric__link").get_by_text(category_name, exact=True).first
                    if await element.is_visible():
                        await element.click()
                        return True
                    else: 
                        print(f"Category {category_name} not found")
                except Exception as e:
                    print(f"Error finding category: {e}")
            return False
        except Exception as e:
            print(f"Error finding category: {e}")
            return False
        
    async def _extract_all_pages_parts_data(self, page: Page) -> list[ScrapedPart]:
        scraped_parts = []
        current_page = 1
        handled_parts = 0
        
        while current_page <= self.pages:
            print(f"Scraping page {current_page}")
            try:
                await page.wait_for_timeout(2000)
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                parts_data, total_parts = await self._extract_parts_data(soup, page.url, page, handled_parts)
                scraped_parts.extend(parts_data)
                handled_parts += total_parts
                
                # Look for pagination and next page button
                next_page_found = await self._navigate_to_next_page(page, soup)
                if not next_page_found:
                    break
                
                current_page += 1
            except Exception as e:
                print(f"Error scraping page {current_page}: {e}")
                break

        return scraped_parts
        
    async def _navigate_to_next_page(self, page: Page, soup: BeautifulSoup) -> bool:
        """Navigate to next page if available"""
        try:
            next_links = soup.select('.page-item.next a')
            if not next_links:
                return False
            
            next_url = next_links[0].get('href')
            if not next_url:
                return False
                
            next_url_str = str(next_url)
            
            await page.goto(next_url_str, timeout=120000, wait_until="networkidle")
            return True
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            return False
        
    async def _extract_parts_data(self, soup: BeautifulSoup, current_url: str, page: Page, handled_parts: int) -> tuple[list[ScrapedPart], int]:
        scraped_parts = []
        
        # Find all product items based on the RIA structure
        parts_elements = soup.select('.ticket-clean')
        
        print(f"Found {len(parts_elements)} product items")
        
        for index, part_element in enumerate(parts_elements):
            try:
                scraped_part = await self._extract_single_part_data_with_details(part_element, current_url, index + 1 + handled_parts, page)
                if scraped_part:
                    scraped_parts.append(scraped_part)
            except Exception as e:
                print(f"Error extracting part data for item {index + 1}: {e}")
                continue
        
        return scraped_parts, len(parts_elements)
    
    async def _extract_single_part_data_with_details(self, part_element, base_url: str, position: int, main_page: Page) -> ScrapedPart | None:
        """
        Extract data for a single part from its HTML element and additional details from product page
        """
        try:
            # First extract basic data from listing
            scraped_part = self._extract_single_part_data(part_element, base_url, position)
            if not scraped_part:
                return None
            
            # Open product page in new tab to get additional details
            product_url = scraped_part.url
            if product_url:
                try:
                    # Create new page in the same context
                    product_page = await main_page.context.new_page()
                    await product_page.goto(product_url, timeout=120000, wait_until="networkidle")
                    
                    # await product_page.wait_for_timeout(2000)
                    
                    # Get product page content
                    product_html = await product_page.content()
                    product_soup = BeautifulSoup(product_html, 'html.parser')
                    
                    # Extract additional details from product page
                    additional_details = self._extract_product_page_details(product_soup)
                    
                    # Merge additional details with basic scraped part data
                    if additional_details:
                        if additional_details.get('warranty_months'):
                            scraped_part.warranty_months = additional_details['warranty_months']

                    images = self._extract_images(product_soup)
                            
                    scraped_part.images = images
                    
                    await product_page.close()
                    
                except Exception as e:
                    print(f"Error extracting product page details for {product_url}: {e}")
                    # Continue with basic data if product page fails
            
            return scraped_part
            
        except Exception as e:
            print(f"Error extracting single part data with details: {e}")
            return None
    
    def _extract_single_part_data(self, part_element, base_url: str, position: int) -> ScrapedPart | None:
        """
        Extract data for a single part from its HTML element using RIA structure
        """
        try:
            # Extract article number
            article_number = self._extract_article_number(part_element)
            
            if not article_number:
                return None
            
            # Extract URL from the title link
            url = self._extract_url(part_element, base_url)
            if not url:
                return None
            
            # Extract title
            title = self._extract_title(part_element)
            if not title:
                return None
            
            # Extract price
            price = self._extract_price(part_element)
            if price is None:
                return None
            
            # Extract availability info
            availability_status = self._extract_availability_status(part_element)
            
            # Extract seller info
            seller_name = self._extract_seller_name(part_element)
            seller_rating = self._extract_seller_rating(part_element)
            
            # Extract location
            location = self._extract_location(part_element)

            # Extract reviews count
            reviews_count = self._extract_reviews_count(part_element)
            
            return ScrapedPart(
                url=url,
                title_on_platform=title,
                article_number=article_number or "N/A",
                price=price,
                availability_status=availability_status or "Available",
                delivery_days=None,  # Not available in RIA structure
                seller_name=seller_name or "RIA",
                seller_rating=seller_rating,
                seller_type="marketplace",
                location=location or "Ukraine",
                warranty_months=None,  # Will be extracted from product page
                reviews_count=reviews_count,
                search_position=position,
                images=[]
            )
            
        except Exception as e:
            print(f"Error extracting single part data: {e}")
            return None
    
    def _extract_url(self, element, base_url: str) -> str | None:
        """Extract product URL from the element"""
        try:
            link_element = element.select_one('.ticket-title')
            if link_element and link_element.get('href'):
                url = link_element.get('href')
                if url.startswith('/'):
                    url = urljoin('https://zapchasti.ria.com', url)
                return url
        except Exception as e:
            print(f"Error extracting URL: {e}")
        return None
    
    def _extract_title(self, element) -> str | None:
        """Extract title from the element"""
        try:
            title_element = element.select_one('.ticket-subtitle')
            if title_element:
                return title_element.get_text(strip=True)
        except Exception as e:
            print(f"Error extracting title: {e}")
        return None
    
    def _extract_article_number(self, element) -> str | None:
        """Extract article number from catalog number holder"""
        try:
            catalog_links = element.select('.catalog-number-holder .link')
            if len(catalog_links) >= 2:
                # The second link is usually the catalog number
                return catalog_links[1].get_text(strip=True)
        except Exception as e:
            print(f"Error extracting article number: {e}")
        return None
    
    def _extract_price(self, element) -> float | None:
        """Extract price from the element"""
        try:
            price_element = element.select_one('.price.js-price .size22')
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Extract numeric value from price text
                price_match = re.search(r'(\d+(?:[\s,]\d+)*)', price_text.replace(' ', ''))
                if price_match:
                    price_str = price_match.group(1).replace(',', '').replace(' ', '')
                    return float(price_str)
        except Exception as e:
            print(f"Error extracting price: {e}")
        return None
    
    def _extract_availability_status(self, element) -> str | None:
        """Extract availability status"""
        try:
            availability_element = element.select_one('.available-label')
            if availability_element:
                return availability_element.get_text(strip=True)
        except Exception as e:
            print(f"Error extracting availability status: {e}")
        return None
    
    def _extract_seller_name(self, element) -> str | None:
        """Extract seller name"""
        try:
            seller_element = element.select_one('.seller__title')
            if seller_element:
                return seller_element.get_text(strip=True)
        except Exception as e:
            print(f"Error extracting seller name: {e}")
        return None
    
    def _extract_seller_rating(self, element) -> float | None:
        """Extract seller rating percentage"""
        try:
            rating_element = element.select_one('.seller__rate')
            if rating_element:
                rating_text = rating_element.get_text(strip=True)
                rating_match = re.search(r'(\d+)', rating_text)
                if rating_match:
                    return float(rating_match.group(1)) / 100.0  # Convert percentage to decimal
        except Exception as e:
            print(f"Error extracting seller rating: {e}")
        return None
    
    def _extract_location(self, element) -> str | None:
        """Extract location"""
        try:
            location_element = element.select_one('.location .address a')
            if location_element:
                return location_element.get_text(strip=True)
        except Exception as e:
            print(f"Error extracting location: {e}")
        return None
    
    def _extract_reviews_count(self, element) -> int | None:
        """Extract reviews count from rating number"""
        try:
            rating_number_element = element.select_one('.rating__number')
            if rating_number_element:
                rating_text = rating_number_element.get_text(strip=True)
                # Extract number from text like "(154)"
                rating_match = re.search(r'\((\d+)\)', rating_text)
                if rating_match:
                    return int(rating_match.group(1))
        except Exception as e:
            print(f"Error extracting reviews count: {e}")
        return None
    
    def _extract_product_page_details(self, product_soup: BeautifulSoup) -> dict:
        """Extract additional details from product page"""
        details = {}
        try:
            # Look for warranty information in technical characteristics
            tech_items = product_soup.select('.technical-list-item')
            for item in tech_items:
                label_element = item.select_one('.label')
                if label_element and 'гарантія' in label_element.get_text(strip=True).lower():
                    value_element = item.select_one('.indent .description-view')
                    if value_element:
                        warranty_text = value_element.get_text(strip=True)
                        # Try to extract months from warranty text
                        warranty_match = re.search(r'(\d+)\s*міс', warranty_text.lower())
                        if warranty_match:
                            details['warranty_months'] = int(warranty_match.group(1))
        except Exception as e:
            print(f"Error extracting product page details: {e}")
        
        return details
    
    def _extract_images(self, product_soup: BeautifulSoup) -> list[str] | None:
        """Extract product images"""
        try:
            images = []
            img_elements = product_soup.select(".slides .slide img")

            for img_element in img_elements:
                if img_element and img_element.get('src'):
                    src = img_element.get('src')
                    images.append(src)
                    
            return images
        except Exception as e:
            print(f"Error extracting images: {e}")
        return None


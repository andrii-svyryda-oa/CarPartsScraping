import re
from urllib.parse import urljoin
from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup

from common.services.scraping.parts.base import BasePartScraper, implements_platform_scraper, ScrapedPart


@implements_platform_scraper("exist")
class ExistsPartScraper(BasePartScraper):
    async def __call__(self) -> list[ScrapedPart]:
        scraped_parts = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()
            
            try:
                # Navigate to the base URL
                await page.goto(self.car_model_platform.platform_url, wait_until="networkidle")
                await page.wait_for_timeout(1000)  # Wait for dynamic content to load
                
                # Find parts category section based on part_category.name
                category_found = await self._find_and_click_category(page, self.part_category.name)
                
                if category_found:
                    # Wait for parts to load after category selection
                    await page.wait_for_timeout(2000)
                    
                    scraped_parts = await self._extract_all_pages_parts_data(page)
                
            except Exception as e:
                print(f"Error scraping Exist website: {e}")
            finally:
                await browser.close()
        
        return scraped_parts
    
    async def _find_and_click_category(self, page, category_name: str) -> bool:
        """
        Find and click on the specified category
        """
        try:
            try:
                element = page.locator(f"[class^='PopularCategoriesstyle__PopularCategoriesList-sc-'] a[aria-label='{category_name}']").first
                if await element.is_visible():
                    await element.click()
                    return True
                else: 
                    print(f"Category {category_name} not found")
            except Exception as e:
                print(f"Error finding category: {e}")

            nav_links = await page.locator("a, button").all()
            for link in nav_links:
                try:
                    text_content = await link.text_content()
                    if text_content and category_name.lower() in text_content.lower():
                        await link.click()
                        return True
                except:
                    continue
                    
            return False
        except Exception as e:
            print(f"Error finding category: {e}")
            return False
        
    async def _extract_all_pages_parts_data(self, page: Page) -> list[ScrapedPart]:
        scraped_parts = []
        current_page = 1
        total_pages = 50
        
        while current_page <= total_pages:
            print(f"Scraping page {current_page}")
            try:
                await page.wait_for_timeout(2000)
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                scraped_parts.extend(self._extract_parts_data(soup, page.url))
                
                next_button_selector = '[aria-label="nextPage"]'
                next_page_button = soup.select_one(next_button_selector)
                
                if not next_page_button or next_page_button.has_attr('disabled'):
                    break

                await page.click(next_button_selector)
                current_page += 1
            except Exception as e:
                print(f"Error scraping page {current_page}: {e}")
                break

        return scraped_parts
        
    def _extract_parts_data(self, soup: BeautifulSoup, current_url: str) -> list[ScrapedPart]:
        scraped_parts = []
        
        parts_elements = soup.select('[class^="Liststyle__CatalogueList-sc-"] [class^="ListItemstyle__CatalogueListItem-"]')
        
        print(f"Found {len(parts_elements)} product items")
        
        for index, part_element in enumerate(parts_elements[:50]):  # Limit to first 50 results
            try:
                scraped_part = self._extract_single_part_data(part_element, current_url, index + 1)
                if scraped_part:
                    scraped_parts.append(scraped_part)
            except Exception as e:
                print(f"Error extracting part data for item {index + 1}: {e}")
                continue
        
        return scraped_parts
    
    def _extract_single_part_data(self, part_element, base_url: str, position: int) -> ScrapedPart | None:
        """
        Extract data for a single part from its HTML element using actual Exist structure
        """
        try:
            # Extract URL from the title link
            url = self._extract_url(part_element, base_url)
            if not url:
                return None
            
            # Extract title from the specific Exist structure
            title = self._extract_title(part_element)
            if not title:
                return None
            
            # Extract article number from the brand/article element
            article_number = self._extract_article_number(part_element)
            
            # Extract price from the specific price container
            price = self._extract_price(part_element)
            if price is None:
                return None
            
            # Extract availability info
            availability_status = self._extract_availability_status(part_element)
            
            # Extract delivery info
            delivery_days = self._extract_delivery_days(part_element)
            
            # Extract brand info
            seller_name = self._extract_seller_name(part_element)
            
            # Extract quantity/stock info
            quantity_info = self._extract_quantity_info(part_element)
            
            # Extract images
            images = self._extract_images(part_element, base_url)
            
            return ScrapedPart(
                url=url,
                title_on_platform=title,
                article_number=article_number or "N/A",
                price=price,
                availability_status=availability_status or "Available",
                delivery_days=delivery_days,
                seller_name=seller_name or "Exist",
                seller_rating=None,  # Not available in the structure
                seller_type="Platform",
                location="Ukraine",
                warranty_months=None,  # Would need to check product details
                reviews_count=None,  # Not visible in listing
                search_position=position,
                images=images
            )
            
        except Exception as e:
            print(f"Error extracting single part data: {e}")
            return None
    
    def _extract_url(self, element, base_url: str) -> str | None:
        """Extract part URL from the title link"""
        # Look for the specific title link in Exist structure
        link = element.select_one('[class^="ListItemTitlestyle__CatalogueListItemTitleLink-sc-"]')
        if link and link.get('href'):
            href = link['href']
            return urljoin(base_url, href) if href.startswith('/') else href
        return None
    
    def _extract_title(self, element) -> str | None:
        """Extract part title from the specific Exist structure"""
        # Try the button first
        title_elem = element.select_one('[class^="ListItemTitlestyle__CatalogueListItemTitleButton-sc-"] strong')
        if title_elem:
            return title_elem.get_text(strip=True)
        
        # Fallback to link
        title_elem = element.select_one('[class^="ListItemTitlestyle__CatalogueListItemTitleLink-sc-"] strong')
        if title_elem:
            return title_elem.get_text(strip=True)
        
        return None
    
    def _extract_article_number(self, element) -> str | None:
        """Extract article number from the brand/article section"""
        # Look for the trademark section that contains brand and article
        trademark_elem = element.select_one('[class^="ListItemTitlestyle__CatalogueListItemTrademark-sc-"]')
        if trademark_elem:
            spans = trademark_elem.find_all('span')
            if len(spans) >= 2:
                # Second span usually contains the article number
                article = spans[1].get_text(strip=True)
                return article.replace(' ', '') if article else None
        
        return None
    
    def _extract_price(self, element) -> float | None:
        """Extract price from the specific Exist price structure"""
        price_elem = element.select_one('[class^="ListItemPricestyle__CatalogueListItemPriceValue-sc-"]')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            # Remove non-breaking spaces and other formatting
            price_text = price_text.replace('\u00a0', '').replace(' ', '').replace(',', '.')
            
            # Extract numeric value
            price_match = re.search(r'(\d+(?:\.\d{2})?)', price_text)
            if price_match:
                try:
                    return float(price_match.group(1))
                except ValueError:
                    pass
        
        return None
    
    def _extract_availability_status(self, element) -> str | None:
        """Extract availability status"""
        # Look for quantity information
        quantity_elem = element.select_one('[class^="ListItemShortInfostyle__ProductQuantityContainer-sc-"]')
        if quantity_elem:
            quantity_text = quantity_elem.get_text(strip=True)
            if quantity_text and quantity_text != '0':
                return "In Stock"
            else:
                return "Out of Stock"
        
        # Check for compatibility indicator (if present, usually means available)
        compat_elem = element.select_one('[class^="ListItemstyle__CatalogueListItemApplicability-sc-"]')
        if compat_elem:
            return "Available"
        
        return "Available"  # Default assumption
    
    def _extract_delivery_days(self, element) -> int | None:
        """Extract delivery information"""
        delivery_elem = element.select_one('[class^="ProductDeliveryInfostyle__ProductDeliveryDay-sc-"]')
        if delivery_elem:
            delivery_text = delivery_elem.get_text(strip=True).lower()
            if 'завтра' in delivery_text:
                return 1
            elif 'сьогодні' in delivery_text:
                return 0
            else:
                # Try to extract number of days
                days_match = re.search(r'(\d+)', delivery_text)
                if days_match:
                    try:
                        return int(days_match.group(1))
                    except ValueError:
                        pass
        
        return None
    
    def _extract_seller_name(self, element) -> str | None:
        """Extract brand/seller name"""
        # Look for brand information
        brand_elem = element.select_one('[class^="ListItemShortInfostyle__CatalogueListItemTrademarkInfo-sc-"]')
        if brand_elem:
            return brand_elem.get_text(strip=True)
        
        # Fallback: extract from trademark section
        trademark_elem = element.select_one('[class^="ListItemTitlestyle__CatalogueListItemTrademark-sc-"] span:first-child')
        if trademark_elem:
            return trademark_elem.get_text(strip=True)
        
        return None
    
    def _extract_quantity_info(self, element) -> str | None:
        """Extract quantity information for debugging"""
        quantity_elem = element.select_one('[class^="ListItemShortInfostyle__ProductQuantityContainer-sc-"]')
        if quantity_elem:
            return quantity_elem.get_text(strip=True)
        return None
    
    def _extract_images(self, element, base_url: str) -> list[str] | None:
        """Extract product images"""
        images = []
        img_element = element.select_one('[class^="ListItemImagestyle__CatalogueListItemImageButton-sc-"] img')
        
        if img_element:
            src = img_element.get('src')
            if src:
                if src.startswith('/'):
                    src = urljoin(base_url, src)
                images.append(src)
        
        return images if images else None

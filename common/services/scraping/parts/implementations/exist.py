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
                await page.goto(self.platform_url, timeout=120000, wait_until="networkidle")
                await page.wait_for_timeout(1000)  # Wait for dynamic content to load
                
                # Find parts category section based on part_category.name
                category_found = await self._find_and_click_category(page, self.category)
                
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
        
        while current_page <= self.pages:
            print(f"Scraping page {current_page}")
            try:
                await page.wait_for_timeout(2000)
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                scraped_parts.extend(await self._extract_parts_data(soup, page.url, page))
                
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
        
    async def _extract_parts_data(self, soup: BeautifulSoup, current_url: str, page: Page) -> list[ScrapedPart]:
        scraped_parts = []
        
        parts_elements = soup.select('[class^="Liststyle__CatalogueList-sc-"] [class^="ListItemstyle__CatalogueListItem-"]')
        
        print(f"Found {len(parts_elements)} product items")
        
        for index, part_element in enumerate(parts_elements):  # Limit to first 50 results
            try:
                scraped_part = await self._extract_single_part_data_with_details(part_element, current_url, index + 1, page)
                if scraped_part:
                    scraped_parts.append(scraped_part)
            except Exception as e:
                print(f"Error extracting part data for item {index + 1}: {e}")
                continue
        
        return scraped_parts
    
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
                    
                    # Get product page content
                    product_html = await product_page.content()
                    product_soup = BeautifulSoup(product_html, 'html.parser')
                    
                    # Extract additional details from product page
                    additional_details = self._extract_product_page_details(product_soup)
                    
                    # Merge additional details with basic scraped part data
                    if additional_details:
                        # Update with additional information
                        if (reviews_count := additional_details.get('reviews_count')) is not None:
                            scraped_part.reviews_count = additional_details['reviews_count']
                        if additional_details.get('seller_rating'):
                            scraped_part.seller_rating = additional_details['seller_rating']
                        if additional_details.get('warranty_months'):
                            scraped_part.warranty_months = additional_details['warranty_months']
                        if additional_details.get('specifications'):
                            # Store specifications in a custom field or update title
                            pass
                    
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
    
    def _extract_product_page_details(self, product_soup: BeautifulSoup) -> dict:
        """
        Extract additional details from product page
        """
        details = {}
        
        try:
            # Extract reviews count and rating
            reviews_count = self._extract_product_reviews_count(product_soup)
            if reviews_count:
                details['reviews_count'] = reviews_count
            
            # Extract detailed specifications
            specifications = self._extract_product_specifications(product_soup)
            if specifications:
                details['specifications'] = specifications
            
            # Extract warranty information from specifications
            warranty = self._extract_warranty_from_specs(specifications)
            if warranty:
                details['warranty_months'] = warranty
                
        except Exception as e:
            print(f"Error extracting product page details: {e}")
        
        return details
    
    def _extract_product_reviews_count(self, soup: BeautifulSoup) -> int | None:
        """Extract reviews count from product page"""
        try:
            selectors = [
                'span:contains("Відгуків")',
            ]
            
            for selector in selectors:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text()
                    # Extract number from text like "12 Відгуків" or "Відгуки (12)"
                    match = re.search(r'(\d+)', text)
                    if match:
                        return int(match.group(1))
        except:
            pass
        return None
    
    def _extract_product_rating(self, soup: BeautifulSoup) -> float | None:
        """Extract product rating from product page"""
        try:
            # Look for rating elements
            rating_selectors = [
                '[class*="Rating"]',
                '[data-rating]',
                '.stars'
            ]
            
            for selector in rating_selectors:
                elem = soup.select_one(selector)
                if elem:
                    # Try to extract rating from data attributes or text
                    rating_attr = elem.get('data-rating')
                    if rating_attr and isinstance(rating_attr, str):
                        try:
                            return float(rating_attr)
                        except:
                            pass
                    
                    # Try to extract from text
                    text = elem.get_text()
                    match = re.search(r'(\d+\.?\d*)', text)
                    if match:
                        try:
                            rating = float(match.group(1))
                            if 0 <= rating <= 5:  # Reasonable rating range
                                return rating
                        except:
                            pass
        except:
            pass
        return None
    
    def _extract_product_specifications(self, soup: BeautifulSoup) -> dict | None:
        """Extract detailed specifications from product page"""
        specifications = {}
        
        try:
            # Find characteristics/specifications tables
            tables = soup.select('[class*="GridTable"] table, [class*="ProductAttributes"] table')
            
            for table in tables:
                if hasattr(table, 'find_all'):
                    rows = table.find_all('tr')
                    for row in rows:
                        if hasattr(row, 'find_all'):
                            cells = row.find_all(['td', 'th'])
                            if len(cells) >= 2:
                                key = cells[0].get_text(strip=True)
                                value = cells[1].get_text(strip=True)
                                if key and value:
                                    specifications[key] = value
        except Exception as e:
            print(f"Error extracting specifications: {e}")
        
        return specifications if specifications else None
    
    def _extract_warranty_from_specs(self, specifications: dict | None) -> int | None:
        """Extract warranty information from specifications"""
        if not specifications:
            return None
        
        try:
            for key, value in specifications.items():
                key_lower = key.lower()
                value_lower = value.lower()
                
                # Look for warranty-related keys
                if any(word in key_lower for word in ['гарантія', 'warranty', 'гарант']):
                    # Extract months from value
                    match = re.search(r'(\d+)', value_lower)
                    if match:
                        number = int(match.group(1))
                        # Convert to months if needed
                        if 'рік' in value_lower or 'year' in value_lower:
                            return number * 12
                        elif 'місяц' in value_lower or 'month' in value_lower:
                            return number
        except:
            pass
        
        return None

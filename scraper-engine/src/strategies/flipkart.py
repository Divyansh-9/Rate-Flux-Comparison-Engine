import asyncio
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from loguru import logger
from src.strategies.base import BaseScraper
from src.config.settings import settings

FLIPKART_SEARCH_URL = "https://www.flipkart.com/search?q={query}"
SCRAPER_API_URL = "http://api.scraperapi.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

class FlipkartScraper(BaseScraper):
    @property
    def retailer_name(self) -> str:
        return "flipkart"

    async def search(self, query: str) -> List[Dict]:
        if not settings.api_key:
            logger.warning(f"[{self.retailer_name}] SCRAPER_API_KEY is missing from environment. Using mock data fallback.")
            logger.info(f"[{self.retailer_name}] searching for '{query}' [MOCKED] ...")
            return self._mock_results(query)
            
        logger.info(f"[{self.retailer_name}] searching for '{query}' via ScraperAPI...")
        return await asyncio.to_thread(self._scrape_with_scraperapi, query)

    def _scrape_with_scraperapi(self, query: str) -> List[Dict]:
        results = []
        target_url = FLIPKART_SEARCH_URL.format(query=quote_plus(query))
        
        # Build ScraperAPI payload
        payload = {
            'api_key': settings.api_key,
            'url': target_url,
            'render': 'true', # Wait for JS execution
            'country_code': 'in' # Flipkart is India-specific
        }
        
        try:
            logger.debug(f"[{self.retailer_name}] Making request to ScraperAPI for: {target_url}")
            response = requests.get(SCRAPER_API_URL, params=payload, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Flipkart has multiple layouts. This matches a common grid list design.
            cards = soup.select("div[data-id]")
            
            logger.info(f"[{self.retailer_name}] found {len(cards)} result cards.")
            
            for card in cards:
                try:
                    # Look for Title
                    title_el = None
                    for selector in ["div.KzDlHZ", "a.WKTcLC", "div._4rR01T"]:
                        title_el = card.select_one(selector)
                        if title_el:
                            break
                            
                    # Look for Price
                    price_el = card.select_one("div.Nx9bqj")
                    if not price_el:
                         price_el = card.select_one("div._30jeq3")

                    # Look for Link 
                    link_el = card.find("a", href=True)

                    # Look for Image
                    img_el = card.select_one("img.DByuf4")
                    if not img_el:
                         img_el = card.select_one("img._396cs4")
                    
                    if not title_el or not price_el or not link_el:
                        continue
                        
                    title = title_el.get_text(strip=True)
                    raw_price = price_el.get_text(strip=True)
                    price = self.normalize_price(raw_price)

                    href = link_el.get("href", "")
                    product_url = f"https://www.flipkart.com{href}" if href else ""

                    image = img_el.get("src", "")

                    results.append({
                        "title": title,
                        "price": price,
                        "source": self.retailer_name,
                        "url": product_url,
                        "image": image or "",
                    })
                except Exception as e:
                    logger.debug(f"[{self.retailer_name}] Error parsing card: {e}")
                    
        except requests.RequestException as e:
            logger.error(f"[{self.retailer_name}] ScraperAPI request error: {e}")
            
        return results

    def _mock_results(self, query: str) -> List[Dict]:
        """Return realistic-looking mock results for development/testing when API key is not present."""
        # Note: Flipkart naturally expects queries in local context. Just creating dummy results.
        return [
            {
                "title": f"Apple {query.title()} (Black Titanium, 128 GB)",
                "price": 134900.00,
                "source": self.retailer_name,
                "url": f"https://www.flipkart.com/apple-iphone-mock/p/mock1",
                "image": f"https://rukminim2.flixcart.com/image/mock1.jpeg",
            },
            {
                "title": f"Apple {query.title()} (Blue Titanium, 256 GB)",
                "price": 144900.00,
                "source": self.retailer_name,
                "url": f"https://www.flipkart.com/apple-iphone-mock/p/mock2",
                "image": f"https://rukminim2.flixcart.com/image/mock2.jpeg",
            },
            {
                "title": f"Apple {query.title()} (Natural Titanium, 512 GB)",
                "price": 164900.00,
                "source": self.retailer_name,
                "url": f"https://www.flipkart.com/apple-iphone-mock/p/mock3",
                "image": f"https://rukminim2.flixcart.com/image/mock3.jpeg",
            },
        ]

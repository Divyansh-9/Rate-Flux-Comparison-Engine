import asyncio
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlencode
from loguru import logger
from src.strategies.base import BaseScraper
from src.config.settings import settings

AMAZON_SEARCH_URL = "https://www.amazon.com/s?k={query}"
SCRAPER_API_URL = "http://api.scraperapi.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

class AmazonScraper(BaseScraper):
    @property
    def retailer_name(self) -> str:
        return "amazon"

    async def search(self, query: str) -> List[Dict]:
        if not settings.api_key:
            logger.warning(f"[{self.retailer_name}] SCRAPER_API_KEY is missing from environment. Using mock data fallback.")
            logger.info(f"[{self.retailer_name}] searching for '{query}' [MOCKED] ...")
            return self._mock_results(query)

        logger.info(f"[{self.retailer_name}] searching for '{query}' via ScraperAPI...")
        return await asyncio.to_thread(self._scrape_with_scraperapi, query)

    def _scrape_with_scraperapi(self, query: str) -> List[Dict]:
        results = []
        target_url = AMAZON_SEARCH_URL.format(query=quote_plus(query))
        
        # Build ScraperAPI payload
        payload = {
            'api_key': settings.api_key,
            'url': target_url,
            'render': 'true', # Wait for JS execution
            'country_code': 'us'
        }
        
        try:
            logger.debug(f"[{self.retailer_name}] Making request to ScraperAPI for: {target_url}")
            response = requests.get(SCRAPER_API_URL, params=payload, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.select("[data-component-type='s-search-result']")
            
            logger.info(f"[{self.retailer_name}] found {len(cards)} result cards.")
            
            for card in cards:
                try:
                    title_el = card.select_one("h2 a span")
                    price_el = card.select_one(".a-price .a-offscreen")
                    link_el = card.select_one("h2 a")
                    img_el = card.select_one("img.s-image")

                    if not title_el or not price_el:
                        continue
                        
                    title = title_el.get_text(strip=True)
                    raw_price = price_el.get_text(strip=True)
                    price = self.normalize_price(raw_price)

                    href = link_el.get("href", "")
                    product_url = f"https://www.amazon.com{href}" if href else ""

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
        slug = query.lower().replace(" ", "-")
        return [
            {
                "title": f"Apple {query.title()} (128GB) - Black Titanium",
                "price": 999.00,
                "source": self.retailer_name,
                "url": f"https://www.amazon.com/dp/B0CHXMYZ2K",
                "image": f"https://m.media-amazon.com/images/I/81Os1SDWpcL._AC_UY218_.jpg",
            },
            {
                "title": f"Apple {query.title()} (256GB) - Blue Titanium",
                "price": 1099.00,
                "source": self.retailer_name,
                "url": f"https://www.amazon.com/dp/B0CHX2TJDY",
                "image": f"https://m.media-amazon.com/images/I/81FxSwRvs3L._AC_UY218_.jpg",
            },
            {
                "title": f"Apple {query.title()} (512GB) - Natural Titanium",
                "price": 1299.00,
                "source": self.retailer_name,
                "url": f"https://www.amazon.com/dp/B0CHWYHXY9",
                "image": f"https://m.media-amazon.com/images/I/81h8EvyA8gL._AC_UY218_.jpg",
            },
        ]

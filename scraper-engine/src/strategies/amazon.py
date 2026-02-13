"""
AmazonStrategy – Concrete strategy for scraping Amazon product listings.

Uses Playwright (async) for browser automation.
Currently returns mock data; swap the mock block with the real
Playwright implementation when ready.
"""

from __future__ import annotations

import asyncio
from urllib.parse import quote_plus

from loguru import logger

from src.strategies.base import BaseScraper

# ── Constants ──
AMAZON_SEARCH_URL = "https://www.amazon.com/s?k={query}"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


class AmazonScraper(BaseScraper):
    """Concrete strategy: Amazon price scraper powered by Playwright."""

    @property
    def retailer_name(self) -> str:
        return "amazon"

    async def search(self, query: str) -> list[dict]:
        logger.info(f"[{self.retailer_name}] searching for '{query}' …")

        # ── Mock data (remove when real scraping is wired up) ──
        results = self._mock_results(query)
        logger.info(f"[{self.retailer_name}] returning {len(results)} results")
        return results

        # ── Real implementation (uncomment when ready) ──
        # return await self._scrape_with_playwright(query)

    # ──────────────────────────────────────────────
    #  Private helpers
    # ──────────────────────────────────────────────

    async def _scrape_with_playwright(self, query: str) -> list[dict]:
        """
        Launch a headless Chromium browser, navigate to Amazon search,
        and extract product cards.
        """
        from playwright.async_api import async_playwright

        results: list[dict] = []
        url = AMAZON_SEARCH_URL.format(query=quote_plus(query))

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=USER_AGENT)
            page = await context.new_page()

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                await page.wait_for_selector(
                    "[data-component-type='s-search-result']", timeout=10_000
                )

                cards = await page.query_selector_all(
                    "[data-component-type='s-search-result']"
                )

                for card in cards:
                    try:
                        title_el = await card.query_selector("h2 a span")
                        price_el = await card.query_selector(".a-price .a-offscreen")
                        link_el = await card.query_selector("h2 a")
                        img_el = await card.query_selector("img.s-image")

                        if not title_el or not price_el:
                            continue

                        title = (await title_el.inner_text()).strip()
                        raw_price = (await price_el.inner_text()).strip()
                        price = self.normalize_price(raw_price)

                        href = await link_el.get_attribute("href") if link_el else ""
                        product_url = f"https://www.amazon.com{href}" if href else ""

                        image = await img_el.get_attribute("src") if img_el else ""

                        results.append(
                            {
                                "title": title,
                                "price": price,
                                "source": self.retailer_name,
                                "url": product_url,
                                "image": image or "",
                            }
                        )
                    except Exception as e:
                        logger.debug(f"Skipping card: {e}")
                        continue

            except Exception as e:
                logger.error(f"[{self.retailer_name}] page error: {e}")
            finally:
                await browser.close()

        return results

    # ──────────────────────────────────────────────
    #  Mock data
    # ──────────────────────────────────────────────

    def _mock_results(self, query: str) -> list[dict]:
        """Return realistic-looking mock results for development/testing."""
        slug = query.lower().replace(" ", "-")
        return [
            {
                "title": f"{query} 128GB – Black",
                "price": 799.99,
                "source": self.retailer_name,
                "url": f"https://www.amazon.com/dp/B0MOCK001/{slug}",
                "image": f"https://m.media-amazon.com/images/I/{slug}-1.jpg",
            },
            {
                "title": f"{query} 256GB – Blue",
                "price": 899.99,
                "source": self.retailer_name,
                "url": f"https://www.amazon.com/dp/B0MOCK002/{slug}",
                "image": f"https://m.media-amazon.com/images/I/{slug}-2.jpg",
            },
            {
                "title": f"{query} Pro Max 512GB – Natural Titanium",
                "price": 1199.99,
                "source": self.retailer_name,
                "url": f"https://www.amazon.com/dp/B0MOCK003/{slug}",
                "image": f"https://m.media-amazon.com/images/I/{slug}-3.jpg",
            },
        ]

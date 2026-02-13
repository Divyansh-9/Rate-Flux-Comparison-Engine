"""
Strategy registry – maps queries to scraper strategies.

To add a new retailer strategy:
  1. Create a class extending BaseStrategy in a new file under strategies/.
  2. Register it in STRATEGIES below.

The `get_strategy()` function picks the right strategy or falls back
to the default aggregated strategy (runs all and merges results).
"""

from loguru import logger

from src.strategies.base import BaseScraper
from src.strategies.amazon import AmazonScraper

# ── Registered strategies ──
STRATEGIES: list[BaseScraper] = [
    AmazonScraper(),
]


class AggregatedStrategy(BaseScraper):
    """
    Default strategy – runs all registered strategies and combines results.
    """

    @property
    def retailer_name(self) -> str:
        return "aggregated"

    async def search(self, query: str) -> list[dict]:
        results: list[dict] = []
        for strategy in STRATEGIES:
            try:
                results.extend(await strategy.search(query))
            except Exception as e:
                logger.error(
                    f"[{strategy.retailer_name}] failed for '{query}': {e}"
                )
        return results


_default = AggregatedStrategy()


def get_strategy(query: str) -> BaseScraper:
    """
    Return a strategy based on the query.

    Override this to add keyword-based routing, e.g.:
        if "amazon" in query.lower():
            return AmazonStrategy()
    """
    _ = query  # available for future routing logic
    return _default

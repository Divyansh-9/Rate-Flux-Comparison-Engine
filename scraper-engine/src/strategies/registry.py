"""
Strategy registry – maps retailer names to scraper strategies.

To add a new retailer strategy:
  1. Create a class extending BaseScraper in a new file under strategies/.
  2. Register it in STRATEGIES below with the retailer name as key.

The `get_strategy()` function returns the appropriate strategy based on
the retailer name or raises an error if the retailer is not supported.
"""

from src.strategies.base import BaseScraper
from src.strategies.amazon import AmazonScraper

# ── Registered strategies ──
STRATEGIES: dict[str, BaseScraper] = {
    "amazon": AmazonScraper(),
    # Add more retailers here:
    # "flipkart": FlipkartScraper(),
    # "ebay": EbayScraper(),
}


def get_strategy(retailer: str) -> BaseScraper:
    """
    Return a scraper strategy based on the retailer name.

    Args:
        retailer: The retailer identifier (e.g., "amazon", "flipkart")

    Returns:
        BaseScraper: The appropriate scraper strategy instance

    Raises:
        ValueError: If the retailer is not supported
    """
    if not retailer:
        raise ValueError("Retailer name cannot be empty")

    retailer_lower = retailer.lower().strip()

    if retailer_lower not in STRATEGIES:
        supported = ", ".join(STRATEGIES.keys())
        raise ValueError(
            f"Unsupported retailer: '{retailer}'. "
            f"Supported retailers: {supported}"
        )

    return STRATEGIES[retailer_lower]


def list_supported_retailers() -> list[str]:
    """Return list of all supported retailer names."""
    return list(STRATEGIES.keys())

"""
Base scraping strategy – abstract interface for all retailer scrapers.

Every concrete strategy **must** implement:
    - retailer_name  (property)
    - search(query)  → list[dict]   (async)

Each dict returned by search() must contain:
    title : str   – product name
    price : float – normalised numeric price
    source: str   – retailer / website name
    url   : str   – direct product link
    image : str   – product image URL
"""

import re
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Abstract strategy interface for all retailer scrapers."""

    # ── Abstract members ──

    @property
    @abstractmethod
    def retailer_name(self) -> str:
        """Human-readable retailer identifier (e.g. 'amazon')."""
        ...

    @abstractmethod
    async def search(self, query: str) -> list[dict]:
        """
        Run an async search/scrape for *query*.

        Returns a list of dicts, each with keys:
            title, price, source, url, image
        """
        ...

    # ── Helper methods ──

    @staticmethod
    def normalize_price(raw: str) -> float:
        """
        Convert a raw price string to a float.

        Handles common currency symbols and thousands separators:
            '$1,299.99'  → 1299.99
            '€ 49,90'    → 49.90   (comma-as-decimal when no dot present)
            '£12.50'     → 12.50
            'Rs. 1,499'  → 1499.0
        """
        if not raw:
            return 0.0

        # Strip currency symbols / words and whitespace
        cleaned = re.sub(r"[^\d.,]", "", raw).strip()

        if not cleaned:
            return 0.0

        # If both ',' and '.' are present, the last one is the decimal sep
        if "," in cleaned and "." in cleaned:
            if cleaned.rfind(",") > cleaned.rfind("."):
                # European: 1.299,99
                cleaned = cleaned.replace(".", "").replace(",", ".")
            else:
                # US/UK: 1,299.99
                cleaned = cleaned.replace(",", "")
        elif "," in cleaned:
            # Ambiguous – treat as decimal only if exactly 2 digits after comma
            parts = cleaned.split(",")
            if len(parts) == 2 and len(parts[1]) == 2:
                cleaned = cleaned.replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")

        try:
            return round(float(cleaned), 2)
        except ValueError:
            return 0.0

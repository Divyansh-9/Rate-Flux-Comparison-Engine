"""Shared utility functions for scrapers."""

from loguru import logger


def sanitize_price(raw: str) -> float:
    """Convert a raw price string like '$1,299.99' to a float."""
    cleaned = (
        raw.replace(",", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .strip()
    )
    try:
        return round(float(cleaned), 2)
    except ValueError:
        logger.warning(f"Could not parse price: {raw}")
        return 0.0

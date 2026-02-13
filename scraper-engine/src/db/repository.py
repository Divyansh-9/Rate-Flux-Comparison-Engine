"""MongoDB persistence for scraped results."""

from datetime import datetime, timezone

from loguru import logger

from src.db.mongo import get_db

COLLECTION = "products"


def save_results(query: str, results: list[dict]) -> None:
    """
    Upsert scraped results into the products collection.

    Each document is keyed by (source, url) to avoid duplicates.
    Expected dict keys: title, price, source, url, image.
    """
    db = get_db()
    collection = db[COLLECTION]
    now = datetime.now(timezone.utc).isoformat()

    for item in results:
        doc = {
            "title": item["title"],
            "price": item["price"],
            "source": item["source"],
            "url": item["url"],
            "image": item["image"],
            "query": query,
            "updated_at": now,
        }

        collection.update_one(
            {"source": item["source"], "url": item["url"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )

    logger.debug(f"Upserted {len(results)} documents for query='{query}'")

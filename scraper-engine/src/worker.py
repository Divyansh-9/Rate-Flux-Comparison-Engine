"""
Scraper Worker – Background process that listens to a Redis queue
and dispatches scrape jobs using the Strategy Pattern.
"""

import asyncio
import json
import signal
import sys
import time

from loguru import logger

from src.config.settings import settings
from src.db.mongo import get_db, close_db
from src.queue.consumer import create_redis_client
from src.strategies.registry import get_strategy
from src.db.repository import save_results

# ── Logging ──
logger.remove()
logger.add(sys.stderr, level=settings.log_level)

running = True


def shutdown(signum, _frame):
    """Graceful shutdown handler."""
    global running
    logger.info(f"Received signal {signum}, shutting down …")
    running = False


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


async def process_job(payload: dict) -> None:
    """Dispatch a single scrape job."""
    query: str = payload.get("query", "").strip()
    if not query:
        logger.warning("Empty query, skipping job")
        return

    logger.info(f"Processing job: query='{query}'")

    # 1. Select Strategy
    strategy = get_strategy(query)
    logger.info(f"Using strategy: {strategy.retailer_name}")

    # 2. Scrape (Async)
    results: list[dict] = await strategy.search(query)

    # 3. Save Results
    if results:
        save_results(query, results)
        logger.info(f"Saved {len(results)} results for '{query}'")
    else:
        logger.warning(f"No results found for '{query}'")


def main() -> None:
    logger.info("Scraper worker starting …")
    logger.info(f"Queue: {settings.queue_name}")

    redis_client = create_redis_client()
    _ = get_db()  # warm connection

    logger.info("Worker ready – waiting for jobs …")

    while running:
        try:
            # BRPOP blocks until a message arrives (timeout = poll interval)
            result = redis_client.brpop(
                settings.queue_name, timeout=settings.queue_poll_interval
            )
            if result is None:
                continue

            _, raw = result
            payload = json.loads(raw)
            asyncio.run(process_job(payload))

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in queue: {e}")
        except Exception as e:
            logger.error(f"Job failed: {e}")
            time.sleep(2)  # back-off on unexpected errors

    # ── Cleanup ──
    redis_client.close()
    close_db()
    logger.info("Worker shut down cleanly.")


if __name__ == "__main__":
    main()

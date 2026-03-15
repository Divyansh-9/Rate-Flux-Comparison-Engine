import asyncio
from src.strategies.amazon import AmazonScraper
from src.strategies.flipkart import FlipkartScraper
import sys
from loguru import logger
import json

logger.remove()
logger.add(sys.stderr, level="DEBUG")

async def main():
    logger.info("Testing Amazon Scraper...")
    amazon = AmazonScraper()
    amazon_res = await amazon.search("macbook pro m3")
    print(json.dumps(amazon_res, indent=2))
    
    logger.info("Testing Flipkart Scraper...")
    flipkart = FlipkartScraper()
    flip_res = await flipkart.search("macbook pro m3")
    print(json.dumps(flip_res, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

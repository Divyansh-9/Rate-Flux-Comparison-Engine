import asyncio
from loguru import logger
from urllib.parse import quote_plus
from playwright.async_api import async_playwright

AMAZON_SEARCH_URL = "https://www.amazon.com/s?k={query}"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

async def main():
    query = "iphone 15 pro"
    url = AMAZON_SEARCH_URL.format(query=quote_plus(query))
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()
        print(f"Navigating to {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_selector("[data-component-type='s-search-result']", timeout=10000)
            print("Found search results")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await page.screenshot(path='screenshot.png')
            print("Saved screenshot.png")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

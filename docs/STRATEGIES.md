# Rate Flux Comparison Engine - Scraper Strategies

This document lists all the active and planned retailer scraping strategies implemented in the Python Scraper Engine.

All strategies inherit from the `BaseScraper` class and implement the `search(query)` method.

---

## 1. Amazon Strategy

The primary strategy for extracting pricing from Amazon.com.

- **Strategy Name:** `AmazonScraper`
- **Retailer Key:** `amazon`
- **Supported Platform:** Amazon.com (`https://www.amazon.com`)
- **Location:** `scraper-engine/src/strategies/amazon.py`

### Input Parameters
- `query` (string): The search term (e.g., "iphone 15").

### Returned Data (Array of Objects)
```json
{
  "title": "iphone 15 128GB – Black",
  "price": 799.99,
  "source": "amazon",
  "url": "https://www.amazon.com/dp/B0MOCK001/iphone-15",
  "image": "https://m.media-amazon.com/images/I/iphone-15-1.jpg"
}
```

### Limitations & Details
- **Current Status:** Uses **ScraperAPI** to bypass aggressive bot protection, falling back to mock JSON results if no `SCRAPER_API_KEY` is present.
- **Method:** Fetches JS-rendered HTML via proxy API, then parses DOM using `BeautifulSoup` matching `data-component-type='s-search-result'`.
- Price normalization handles commas and dollar signs natively via Base class.

### Example Usage (from API)
```json
// POST /api/scrape
{ "query": "iphone 15", "retailer": "amazon" }
```

---

## 2. Flipkart Strategy

The strategy for extracting pricing from Flipkart (India).

- **Strategy Name:** `FlipkartScraper`
- **Retailer Key:** `flipkart`
- **Supported Platform:** Flipkart (`https://www.flipkart.com`)
- **Location:** `scraper-engine/src/strategies/flipkart.py`

### Input Parameters
- `query` (string): The search term (e.g., "iphone 15").

### Returned Data (Array of Objects)
```json
{
  "title": "Apple iPhone 15 (Black, 128 GB)",
  "price": 65999.00,
  "source": "flipkart",
  "url": "https://www.flipkart.com/apple-iphone-15-black/p/itm...",
  "image": "https://rukminim2.flixcart.com/image/...jpg"
}
```

### Limitations & Details
- **Current Status:** Actively implemented. Uses **ScraperAPI** with India-focused geo-targeting (`country_code=in`) to bypass 403 Forbidden errors, falling back to mock JSON if no API key is present.
- **Method:** Parse JS-rendered proxy response using `BeautifulSoup`, dynamically matching multiple potential grid/list class layouts (`div.KzDlHZ`, `a.WKTcLC`).

---

*(Note: Automatically append new strategies here as they are added to `src/strategies/`)*

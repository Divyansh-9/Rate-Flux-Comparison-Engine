# Scraper Engine (Python Worker)

> High-performance web scraping worker using Playwright and the Strategy Pattern

## 📋 Overview

The scraper engine is a Python-based background worker that consumes scrape jobs from Redis, executes retailer-specific scraping strategies using Playwright, normalizes product data, and persists results to MongoDB.

## 🏗️ Architecture

```
src/
├── worker.py                  # Main worker loop (BRPOP)
├── config/                    # Configuration
│   ├── __init__.py
│   └── settings.py           # Environment variables
├── strategies/               # Scraper implementations
│   ├── __init__.py
│   ├── base.py              # Abstract BaseScraper
│   ├── registry.py          # Strategy resolver
│   ├── amazon.py            # Amazon scraper (Phase 2)
│   └── flipkart.py          # Flipkart scraper (Phase 3)
├── queue/                    # Redis consumer
│   ├── __init__.py
│   └── consumer.py          # Job consumption logic
├── db/                       # Database layer
│   ├── __init__.py
│   ├── mongo.py             # MongoDB connection
│   └── repository.py        # Data persistence
└── utils/                    # Utilities
    ├── __init__.py
    └── helpers.py           # Helper functions
```

### Design Pattern: Strategy Pattern

```python
Worker Loop (BRPOP)
       ↓
Job Received: {query: "iphone 15"}
       ↓
Registry.resolve(query) → AmazonScraper
       ↓
AmazonScraper.scrape(query)
       ↓
Normalize Data
       ↓
Repository.save(products)
       ↓
MongoDB
```

**Why Strategy Pattern?**
- ✅ Add new retailers without modifying core logic
- ✅ Each scraper is isolated and testable
- ✅ Easy to swap implementations
- ✅ Follows Open/Closed Principle

## 🛠️ Technology Stack

- **Runtime:** Python 3.11
- **Scraping:** Playwright (Chromium)
- **Queue:** redis-py
- **Database:** pymongo
- **Async:** asyncio
- **Parsing:** BeautifulSoup4 (if needed)
- **Config:** python-dotenv

## 🎯 Core Responsibilities

### Phase 1 (Foundation)
- ✅ Python project structure
- ⬜ BaseScraper abstract class
- ⬜ Strategy registry implementation
- ⬜ Redis consumer setup
- ⬜ MongoDB repository layer
- ⬜ Configuration management

### Phase 2 (MVP)
- ⬜ Playwright setup
- ⬜ Amazon scraper strategy
- ⬜ Product normalization logic
- ⬜ Worker main loop (BRPOP)
- ⬜ Error handling and retries
- ⬜ Logging setup

### Phase 3 (Production)
- ⬜ Flipkart scraper strategy
- ⬜ Additional retailer strategies
- ⬜ Proxy rotation
- ⬜ User-agent rotation
- ⬜ CAPTCHA handling
- ⬜ Rate limiting per retailer
- ⬜ Distributed scraping
- ⬜ Monitoring and alerting

## 🚀 Getting Started

### Installation

```bash
cd scraper-engine
pip install -r requirements.txt
python -m playwright install chromium
```

### Environment Variables

```env
REDIS_URL=redis://localhost:6379
MONGO_URI=mongodb://localhost:27017/price-comparison
LOG_LEVEL=INFO
HEADLESS=true
```

### Run Worker

```bash
python -m src.worker
# Worker starts listening on scrape:jobs queue
```

### Docker

```bash
docker build -t price-comparison-scraper .
docker run price-comparison-scraper
```

## 📐 Strategy Pattern Implementation

### BaseScraper (Abstract Class)

```python
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    @property
    @abstractmethod
    def retailer_name(self) -> str:
        """Return the retailer identifier (e.g., 'amazon', 'flipkart')"""
        pass
    
    @abstractmethod
    async def scrape(self, query: str) -> List[Dict]:
        """
        Scrape products for the given query.
        Returns list of normalized product dictionaries.
        """
        pass
    
    def normalize(self, raw_data: Dict) -> Dict:
        """Normalize raw scraped data to common schema"""
        return {
            'title': raw_data.get('title'),
            'price': self._parse_price(raw_data.get('price')),
            'url': raw_data.get('url'),
            'retailer': self.retailer_name,
            'imageUrl': raw_data.get('image'),
            'rating': raw_data.get('rating'),
        }
```

### AmazonScraper (Concrete Strategy)

```python
class AmazonScraper(BaseScraper):
    @property
    def retailer_name(self) -> str:
        return 'amazon'
    
    async def scrape(self, query: str) -> List[Dict]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Navigate to search
            await page.goto(f'https://amazon.com/s?k={query}')
            
            # Extract product data
            products = await page.query_selector_all('.s-result-item')
            results = []
            
            for product in products:
                raw = await self._extract_product(product)
                normalized = self.normalize(raw)
                results.append(normalized)
            
            await browser.close()
            return results
```

### Strategy Registry

```python
from typing import Dict, Type

SCRAPER_STRATEGIES: Dict[str, Type[BaseScraper]] = {
    'amazon': AmazonScraper,
    'flipkart': FlipkartScraper,  # Phase 3
}

def get_scraper(query: str) -> BaseScraper:
    """Resolve which scraper to use based on query or logic"""
    # For now, default to Amazon
    # In Phase 3, add intelligent routing
    return SCRAPER_STRATEGIES['amazon']()
```

## 🔄 Worker Loop

```python
import redis
import json
from strategies.registry import get_scraper
from db.repository import save_products

def main():
    r = redis.Redis.from_url(REDIS_URL)
    
    while True:
        # Blocking pop from queue
        _, job = r.brpop('scrape:jobs')
        data = json.loads(job)
        query = data['query']
        
        try:
            # Get appropriate scraper
            scraper = get_scraper(query)
            
            # Scrape products
            products = await scraper.scrape(query)
            
            # Save to MongoDB
            save_products(products, query)
            
            print(f"✓ Scraped {len(products)} products for '{query}'")
        
        except Exception as e:
            print(f"✗ Error scraping '{query}': {e}")
            # TODO: Retry logic, dead letter queue
```

## 🗄️ Data Normalization

### Input (Raw Amazon Data)
```python
{
    'title': 'Apple iPhone 15 Pro (128GB)',
    'price': '$999.00',
    'url': 'https://amazon.com/dp/B0...',
    'image': 'https://m.media-amazon.com/...',
    'stars': '4.5',
}
```

### Output (Normalized)
```python
{
    'title': 'Apple iPhone 15 Pro (128GB)',
    'price': 999.0,  # Parsed float
    'url': 'https://amazon.com/dp/B0...',
    'retailer': 'amazon',
    'imageUrl': 'https://m.media-amazon.com/...',
    'rating': 4.5,
    'query': 'iphone 15',
    'scrapedAt': '2026-02-13T10:30:00Z',
}
```

## 🧪 Testing

```bash
# Unit tests
pytest tests/

# Test specific scraper
pytest tests/strategies/test_amazon.py

# Manual test
python -c "from src.strategies.amazon import AmazonScraper; import asyncio; asyncio.run(AmazonScraper().scrape('iphone'))"
```

## 🚧 Anti-Bot Evasion (Phase 3)

### Proxy Rotation
```python
proxies = ['proxy1.com', 'proxy2.com']
proxy = random.choice(proxies)
browser = await p.chromium.launch(proxy={'server': proxy})
```

### User-Agent Rotation
```python
user_agents = ['Mozilla/5.0...', 'Mozilla/5.0...']
page.set_extra_http_headers({'User-Agent': random.choice(user_agents)})
```

### Rate Limiting
```python
import time
time.sleep(random.uniform(2, 5))  # Random delay between requests
```

## 📦 Dependencies

### Core
```txt
playwright==1.40.0
redis==5.0.0
pymongo==4.6.0
python-dotenv==1.0.0
```

### Dev
```txt
pytest==7.4.0
black==23.12.0
mypy==1.7.0
```

## 🗺️ Roadmap

### Phase 2 Tasks
- [ ] Implement BaseScraper abstract class
- [ ] Create strategy registry
- [ ] Build Amazon scraper with Playwright
- [ ] Implement Redis consumer (BRPOP)
- [ ] Connect MongoDB repository
- [ ] Add product normalization
- [ ] Implement error handling
- [ ] Add structured logging

### Phase 3 Tasks
- [ ] Add Flipkart scraper strategy
- [ ] Implement proxy rotation
- [ ] Add user-agent rotation
- [ ] Handle CAPTCHAs
- [ ] Add retry logic with exponential backoff
- [ ] Implement rate limiting per retailer
- [ ] Add distributed scraping support
- [ ] Implement monitoring and alerting
- [ ] Add performance metrics

## 📊 Performance Considerations

- **Headless Mode:** Run browsers in headless mode for speed
- **Concurrent Scraping:** Use asyncio for parallel scraping
- **Connection Pooling:** Reuse browser contexts
- **Resource Limits:** Limit concurrent browsers to avoid memory issues

## 🔒 Ethical Scraping

- ✅ Respect robots.txt
- ✅ Rate limit requests
- ✅ Don't overload servers
- ✅ Use official APIs when available
- ✅ Cache results to minimize requests

## 📝 Change Log

### 2026-02-13
- Enhanced documentation
- Documented Strategy Pattern architecture
- Added comprehensive implementation examples
- Outlined all three phases

### 2026-02-11
- Initial Python service scaffold created
- Basic project structure established
- Requirements file created

---

**Status:** 🟡 Phase 1 - Foundation Setup

[← Back to Main README](../README.md)

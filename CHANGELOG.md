# Rate Flux Comparison Engine - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Integrated **ScraperAPI** proxy logic into `amazon.py` and `flipkart.py` to bypass proactive bot blocking and connection dropped errors.
- Built an intelligent "Mock Fallback" system in the scraper strategies to return dummy data if `SCRAPER_API_KEY` is not provided in `.env`.
- Added support for `requests` and `BeautifulSoup` parsing across Amazon and Flipkart grids.
- Implemented **Zod Data Validation** (`zod`) middleware on product retrieval endpoints.
- Added **Redis Cache-Aside** architectural pattern to `/api/products/search` (5m TTL).
- Created `test_e2e.py` to systematically test API architecture, caching speeds, and error handling.

### Fixed
- Fixed critical `Dockerfile` entrypoint bug (was pointing to non-existent `src.main` instead of `src.worker`).
- Fixed critical `worker.py` routing bug where the search query was mistakenly being used to look up the scraper strategy instead of the specified `retailer`.
- Fixed several TypeScript compilation mismatch errors inside `redis.ts` and `scrape.routes.ts` that were preventing the API Docker container from successfully building.

### Changed
- **[BREAKING]** Removed local Playwright dependency logic for scraping in favor of upstream proxy API HTML fetching.
- Centralized `docs/` folder implementing the new `@[/documentation-intelligence-system]` (API, Architecture, Strategies).

## [2026-02-13] - Evening

### Changed
- **[BREAKING]** Changed job payload to require `retailer` field. The API now expects `{ "query": string, "retailer": "amazon" | "flipkart" }`.
- **[BREAKING]** Refactored Scraper Engine worker to use a persistent `asyncio` event loop instead of re-creating loops per job.
- Switched from query-based to explicit retailer-based strategy routing.
- Removed `AggregatedStrategy` pattern (which ran all scrapers concurrently). Worker now expects a 1:1 mapping of job to retailer.

### Added
- Implemented non-blocking Redis `BRPOP` consumer using `ThreadPoolExecutor` to unblock Playwright.
- Added abstract `BaseScraper` class with native price normalizer.
- Added Flipkart scraper scaffold (mock implementation).
- Added architectural evolution log to README.

### Fixed
- Enhanced worker error handling with granular try-catch blocks.
- Added proper resource cleanup with `try-finally` blocks in Python.

## [2026-02-13] - Afternoon

### Added
- Initial setup of API routing and worker dependencies.
- Added comprehensive documentation across service READMEs.
- Installed `npm` and `ioredis` in the Express container.

## [2026-02-11]

### Added
- Initial monorepo scaffold created.
- Base Next.js, Express, and Python architecture generated.
- `docker-compose.yml` configuration added.

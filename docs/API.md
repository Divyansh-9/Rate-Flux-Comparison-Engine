# Rate Flux Comparison Engine - API Documentation

This document describes the Express REST API endpoints available in the system.

## Base URL
All API requests are routed through `/api`. The default local development server runs on `http://localhost:5000`.

---

## 1. Scrape Jobs

### Enqueue Scrape Job
Creates a new async scraping job in the Redis queue for the background worker to process.

- **Endpoint:** `/api/scrape`
- **Method:** `POST`

#### Parameters (JSON Body)
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | The product search term (max 200 chars). |
| `retailer` | enum | Yes | The target retailer. Supported: `"amazon"`, `"flipkart"`. |

#### Response Schema
- **Status:** `202 Accepted`

```json
{
  "message": "Scrape job queued",
  "query": "iphone 15",
  "retailer": "amazon"
}
```

#### Example Usage
```bash
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"query": "iphone 15", "retailer": "amazon"}'
```

---

## 2. Products

### Get All Products
Retrieves all scraped products from the MongoDB storage.

- **Endpoint:** `/api/products`
- **Method:** `GET`

### Search Products
Searches against the existing stored products.

- **Endpoint:** `/api/products/search`
- **Method:** `GET`

### Get Product By ID
Retrieves a specific product detail.

- **Endpoint:** `/api/products/:id`
- **Method:** `GET`

---

## 3. System Health

### Health Check
Validates that the API server is running and responding.

- **Endpoint:** `/health`
- **Method:** `GET`

#### Response Schema
- **Status:** `200 OK`

```json
{
  "status": "ok",
  "timestamp": "2026-03-14T09:15:30.000Z"
}
```

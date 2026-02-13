# API Service (Express + TypeScript)

> RESTful API service orchestrating the price comparison engine

## 📋 Overview

The API service is the central orchestration layer built with Express and TypeScript. It handles incoming requests from the client, manages job queuing to Redis, and retrieves product data from MongoDB.

## 🏗️ Architecture

```
src/
├── index.ts                # Server entry point
├── config/                 # Configuration management
│   ├── index.ts           # Centralized config
│   └── db.ts              # Database config
├── controllers/           # Request handlers
│   └── product.controller.ts
├── services/              # Business logic
│   ├── product.service.ts
│   └── queue.service.ts
├── models/                # MongoDB models
│   └── product.model.ts
├── routes/                # Route definitions
│   ├── health.routes.ts
│   ├── product.routes.ts
│   └── scrape.routes.ts
├── lib/                   # External clients
│   └── redis.ts          # Redis client & queue functions
├── middleware/           # Express middleware
│   └── errorHandler.ts  # Global error handler
└── utils/               # Utilities
    └── helpers.ts       # Helper functions
```

### Design Pattern: MVC + Service Layer

```
Request → Route → Controller → Service → Model → Database
                                    ↓
                                  Redis Queue
```

## 🛠️ Technology Stack

- **Runtime:** Node.js 20
- **Framework:** Express 4
- **Language:** TypeScript
- **Database:** MongoDB (via Mongoose)
- **Queue/Cache:** Redis (via ioredis)
- **Validation:** Zod (planned)
- **Package Manager:** npm

## 🎯 Core Responsibilities

### Phase 1 (Foundation)
- ✅ Express server setup
- ✅ TypeScript configuration
- ✅ Redis integration (ioredis)
- ⬜ MongoDB connection
- ⬜ Health check endpoint
- ⬜ Error handling middleware

### Phase 2 (MVP)
- ⬜ POST `/api/scrape` - Enqueue scrape job
- ⬜ GET `/api/products` - Search products
- ⬜ Product service layer
- ⬜ MongoDB schema and models
- ⬜ Request validation
- ⬜ CORS configuration

### Phase 3 (Production)
- ⬜ Rate limiting
- ⬜ Authentication (JWT)
- ⬜ Request logging
- ⬜ API documentation (Swagger)
- ⬜ Caching strategy
- ⬜ Monitoring endpoints
- ⬜ Graceful shutdown

## 🚀 Getting Started

### Installation

```bash
cd api
npm install
```

### Environment Variables

```env
PORT=5000
MONGO_URI=mongodb://localhost:27017/price-comparison
REDIS_URL=redis://localhost:6379
NODE_ENV=development
```

### Development Server

```bash
npm run dev
# Server runs on http://localhost:5000
```

### Production Build

```bash
npm run build
npm start
```

### Docker

```bash
docker build -t price-comparison-api .
docker run -p 5000:5000 price-comparison-api
```

## 📡 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-02-13T10:30:00Z",
  "services": {
    "mongo": "connected",
    "redis": "connected"
  }
}
```

### Trigger Scrape Job
```http
POST /api/scrape
Content-Type: application/json

{
  "query": "iphone 15"
}
```

**Response:**
```json
{
  "jobId": "job_123",
  "message": "Scrape job queued successfully"
}
```

### Search Products
```http
GET /api/products?query=iphone&limit=20&offset=0
```

**Response:**
```json
{
  "products": [
    {
      "id": "prod_123",
      "title": "iPhone 15 Pro",
      "price": 999.99,
      "retailer": "amazon",
      "url": "https://amazon.com/...",
      "imageUrl": "https://...",
      "createdAt": "2026-02-13T10:00:00Z"
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

## 🗄️ Database Schema

### Product Model

```typescript
interface Product {
  _id: ObjectId;
  title: string;
  price: number;
  retailer: string;  // 'amazon' | 'flipkart'
  url: string;
  imageUrl?: string;
  rating?: number;
  reviewCount?: number;
  query: string;      // Search term
  scrapedAt: Date;
  createdAt: Date;
  updatedAt: Date;
}
```

### Indexes
- `query` (text index for search)
- `retailer` (filter by retailer)
- `price` (sort by price)
- `createdAt` (sort by freshness)

## 📦 Key Files

### `src/lib/redis.ts`
Redis client and queue operations

```typescript
export async function enqueueScrapeJob(query: string): Promise<void> {
  const payload = JSON.stringify({ 
    query, 
    createdAt: new Date().toISOString() 
  });
  await getRedis().lpush(SCRAPE_QUEUE, payload);
}
```

### `src/controllers/product.controller.ts`
Request handlers

```typescript
export async function searchProducts(req: Request, res: Response) {
  const { query, limit, offset } = req.query;
  const products = await productService.search(query, limit, offset);
  res.json(products);
}
```

### `src/services/product.service.ts`
Business logic

```typescript
export class ProductService {
  async search(query: string, limit: number, offset: number) {
    return Product.find({ query })
      .limit(limit)
      .skip(offset)
      .sort({ price: 1 });
  }
}
```

## 🧪 Testing

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# Test queue
ts-node scripts/test-queue.ts
```

## 📊 Performance Considerations

- **Connection Pooling:** MongoDB and Redis connections are reused
- **Caching:** Redis caches frequently accessed products
- **Indexing:** MongoDB indexes on query fields
- **Pagination:** Limit response sizes with pagination

## 🔒 Security

### Planned (Phase 3)
- Rate limiting (express-rate-limit)
- CORS configuration
- Request validation (Zod)
- Environment variable validation
- Helmet.js for security headers

## 📦 Dependencies

### Core
- `express` - Web framework
- `typescript` - Type safety
- `ioredis` - Redis client
- `mongoose` - MongoDB ODM (planned)

### Dev Dependencies
- `ts-node` - TypeScript execution
- `nodemon` - Auto-restart
- `@types/*` - Type definitions

## 🗺️ Roadmap

### Phase 2 Tasks
- [ ] Connect MongoDB with Mongoose
- [ ] Implement Product model and schema
- [ ] Build scrape endpoint (POST /api/scrape)
- [ ] Build search endpoint (GET /api/products)
- [ ] Add request validation with Zod
- [ ] Implement error handling middleware
- [ ] Add CORS configuration

### Phase 3 Tasks
- [ ] Add rate limiting
- [ ] Implement JWT authentication
- [ ] Add Swagger API documentation
- [ ] Implement caching strategy
- [ ] Add request logging (Winston)
- [ ] Add monitoring (Prometheus/Datadog)
- [ ] Implement graceful shutdown
- [ ] Add integration tests

## 📝 Change Log

### 2026-02-13
- Installed ioredis dependency
- Enhanced documentation
- Added comprehensive API specifications
- Documented all three phases

### 2026-02-11
- Express service scaffold created
- TypeScript configuration added
- Basic route structure established
- Redis integration started

---

**Status:** 🟡 Phase 1 - Redis Integration Complete

[← Back to Main README](../README.md)

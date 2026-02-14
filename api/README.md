# API Service (Express + TypeScript)

> RESTful API service orchestrating the price comparison engine

## 📋 Overview

The API service is the central orchestration layer built with Express and TypeScript. It handles incoming requests from the client, publishes scrape jobs to Redis queue with structured payloads, and retrieves product data from MongoDB.

**Core Responsibilities:**
- ✅ Accept scrape requests from frontend
- ✅ Publish structured job payloads to Redis queue
- ✅ Serve cached product results from MongoDB
- ✅ Validate request parameters
- ✅ Handle errors and provide meaningful responses

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
Request → Route → Controller → Service → Model → MongoDB
                                    ↓
                            Redis Queue (Publisher)
                                    ↓
                        Job: {query, retailer}
```

**Key Architectural Decisions:**
- **Queue-based decoupling:** API doesn't wait for scraping to complete
- **Structured payloads:** Explicit `{query, retailer}` contract
- **Document storage:** MongoDB for flexible product schemas
- **Connection pooling:** Reused connections for performance

## 🛠️ Technology Stack

- **Runtime:** Node.js 20
- **Framework:** Express 4
- **Language:** TypeScript
- **Database:** MongoDB (via Mongoose)
- **Queue:** Redis (via ioredis) - Publisher only
- **Validation:** Zod (planned)
- **Package Manager:** npm

**Why These Choices:**
- **Express:** Mature, lightweight, extensive middleware ecosystem
- **MongoDB:** Document-based storage suits variable product schemas from different retailers
- **Redis Queue:** Decouples API from scraping worker, enables async processing
- **Mongoose:** Type-safe MongoDB ODM with schema validation

## 🎯 Core Responsibilities

### Phase 1 (Foundation)
- ✅ Express server setup
- ✅ TypeScript configuration
- ✅ Redis integration (ioredis)
- ✅ Queue publishing with structured payloads
- ⬜ MongoDB connection with Mongoose
- ⬜ Health check endpoint
- ⬜ Error handling middleware

### Phase 2 (MVP)
- ⬜ POST `/api/scrape` - Publish scrape jobs with retailer
- ⬜ GET `/api/products` - Search products from MongoDB
- ⬜ Product service layer
- ⬜ Mongoose schemas and models
- ⬜ Request validation with Zod
- ⬜ CORS configuration
- ⬜ MongoDB indexes for performance

### Phase 3 (Production)
- ⬜ Rate limiting per IP
- ⬜ Authentication (JWT)
- ⬜ Request logging (Winston)
- ⬜ API documentation (Swagger)
- ⬜ Response caching strategy
- ⬜ Health metrics endpoint
- ⬜ Graceful shutdown
- ⬜ Integration tests

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
  "query": "iphone 15",
  "retailer": "amazon"
}
```

**Request Body:**
- `query` (string, required): Search term
- `retailer` (string, required): Retailer to scrape. Supported: `amazon`, `flipkart`

**Response:**
```json
{
  "jobId": "job_123",
  "message": "Scrape job queued successfully",
  "retailer": "amazon"
}
```

**Error Response (Invalid Retailer):**
```json
{
  "error": "Unsupported retailer: ebay. Supported retailers: amazon, flipkart"
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
Redis client and queue publishing

```typescript
export async function enqueueScrapeJob(
  query: string, 
  retailer: string
): Promise<void> {
  const payload = JSON.stringify({ 
    query,
    retailer,
    createdAt: new Date().toISOString() 
  });
  await getRedis().lpush(SCRAPE_QUEUE, payload);
}
```

**Key Points:**
- Uses `LPUSH` to add jobs to queue (worker uses `BRPOP` to consume)
- Payload is **structured** with explicit `retailer` field
- Includes `createdAt` timestamp for job tracking

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

# Test queue publishing
ts-node scripts/test-queue.ts
```

**Test Queue Script Example:**
```typescript
// scripts/test-queue.ts
import { enqueueScrapeJob } from '../src/lib/redis';

async function testQueue() {
  await enqueueScrapeJob('iphone 15', 'amazon');
  console.log('✓ Job published to queue');
}

testQueue();
```

---

## 📤 Queue Publishing Contract

### Structured Job Payload

The API publishes jobs to Redis queue `scrape:jobs` with the following structure:

```json
{
  "query": "iphone 15",
  "retailer": "amazon",
  "createdAt": "2026-02-13T10:30:00.000Z"
}
```

**Field Specifications:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `string` | ✅ Yes | User's search term |
| `retailer` | `string` | ✅ Yes | Target retailer (`amazon`, `flipkart`) |
| `createdAt` | `string` (ISO 8601) | ✅ Yes | Job creation timestamp |

### Publishing Flow

```typescript
// 1. Client sends request
POST /api/scrape
{
  "query": "iphone 15",
  "retailer": "amazon"
}

// 2. API validates request
if (!query || !retailer) {
  return res.status(400).json({ error: 'Missing required fields' });
}

// 3. API publishes to Redis
await redis.lpush('scrape:jobs', JSON.stringify({
  query,
  retailer,
  createdAt: new Date().toISOString()
}));

// 4. API responds immediately
res.json({ 
  message: 'Job queued',
  jobId: generateJobId() 
});

// 5. Worker picks up job asynchronously (in background)
```

### Why Queue-Based Decoupling?

#### Without Queue (Synchronous)
```
❌ Client → API → [Wait for scraping...] → Response
   - API blocks for 10-30 seconds
   - Timeout issues
   - Poor user experience
   - Can't scale workers independently
```

#### With Queue (Asynchronous)
```
✅ Client → API → Redis Queue → Response (immediate)
                      ↓
                   Worker (async)
                      ↓
                   MongoDB
```

**Benefits:**

1. **Instant Response**
   - API returns immediately (~10ms)
   - Client doesn't wait for scraping
   - Better UX

2. **Fault Tolerance**
   - Jobs persist in Redis if worker crashes
   - No lost requests
   - Can retry failed jobs

3. **Independent Scaling**
   - Scale API horizontally (request handling)
   - Scale workers horizontally (scraping capacity)
   - Different resource requirements

4. **Rate Limiting**
   - Control scraping rate to avoid bans
   - Queue acts as buffer
   - Workers process at safe pace

5. **Load Balancing**
   - Multiple workers consume same queue
   - Redis `BRPOP` is atomic (no duplication)
   - Automatic distribution

6. **Technology Decoupling**
   - API in Node.js (fast I/O)
   - Worker in Python (Playwright support)
   - Best tool for each job

### Monitoring Queue Health

```typescript
// Check queue depth
const queueLength = await redis.llen('scrape:jobs');

if (queueLength > 1000) {
  console.warn('Queue backlog detected, scale workers');
}
```

**Metrics to Track:**
- Queue depth (jobs waiting)
- Processing rate (jobs/minute)
- Failed jobs (DLQ)
- Average wait time

---

## 📊 Performance Considerations

- **Connection Pooling:** MongoDB and Redis connections are reused
- **Queue-Based Async:** API responds instantly, scraping happens in background
- **MongoDB Indexes:** Query, retailer, and price fields indexed for fast lookups
- **Pagination:** Limit response sizes with offset-based pagination
- **No Blocking Operations:** All I/O is non-blocking (async/await throughout)

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

### 2026-02-13 (Evening) - Queue Publishing & MongoDB Migration
- **[BREAKING]** Updated `enqueueScrapeJob()` to require both `query` and `retailer` parameters
- **[ARCHITECTURE]** Clarified API role as Redis queue publisher (not consumer)
- Added "Queue Publishing Contract" section with detailed payload specification
- Documented queue-based decoupling benefits (6 key advantages)
- Added queue monitoring guidance
- Updated all code examples to include `retailer` field
- Enhanced architecture diagram showing structured payload flow
- Removed references to relational databases (fully committed to MongoDB)
- Added "Why These Choices" rationale for technology stack
- Updated Phase 1 checklist to reflect queue publishing completion

### 2026-02-13 (Afternoon) - Documentation Enhancement
- Installed ioredis dependency
- Enhanced documentation structure
- Added comprehensive API endpoint specifications
- Documented all three development phases
- Added database schema with MongoDB indexes

### 2026-02-11 - Initial Scaffold
- Express service scaffold created
- TypeScript configuration added
- Basic route structure established
- Redis integration started

---

**Status:** 🟡 Phase 1 - Redis Integration Complete

[← Back to Main README](../README.md)

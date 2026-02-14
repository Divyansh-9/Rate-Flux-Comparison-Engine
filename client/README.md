# Client Service (Next.js Frontend)

> Modern, server-side rendered frontend for the Price Comparison Engine

## 📋 Overview

The client service is a Next.js 14 application using the App Router that provides a fast, SEO-friendly interface for users to search and compare product prices across multiple retailers.

## 🏗️ Architecture

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page (search)
│   ├── products/          # Product listing pages
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── SearchBar/        # Search input component
│   ├── ProductCard/      # Product display card
│   ├── PriceChart/       # Price history visualization (Phase 3)
│   └── FilterPanel/      # Filtering UI (Phase 3)
├── lib/                  # Utilities & API client
│   └── api.ts           # API service wrapper
└── types/               # TypeScript definitions
    └── index.ts         # Shared types
```

## 🛠️ Technology Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS (planned)
- **Animations:** GSAP (Phase 3)
- **State Management:** React Context / Zustand (Phase 3)
- **HTTP Client:** fetch API
- **Package Manager:** npm

## 🎯 Core Responsibilities

### Phase 1 (Foundation)
- ✅ Next.js setup with App Router
- ✅ TypeScript configuration
- ⬜ Basic routing structure
- ⬜ API client wrapper

### Phase 2 (MVP)
- ⬜ Search bar component
- ⬜ Product listing page
- ⬜ ProductCard component
- ⬜ Loading states
- ⬜ Error handling
- ⬜ API integration

### Phase 3 (Production)
- ⬜ Tailwind CSS integration
- ⬜ GSAP animations
- ⬜ Advanced filtering UI
- ⬜ Price history charts
- ⬜ Responsive design
- ⬜ SEO optimization
- ⬜ Performance optimization
- ⬜ Progressive Web App features

## 🚀 Getting Started

### Installation

```bash
cd client
npm install
```

### Development Server

```bash
npm run dev
# Open http://localhost:3000
```

### Build for Production

```bash
npm run build
npm start
```

### Docker

```bash
docker build -t price-comparison-client .
docker run -p 3000:3000 price-comparison-client
```

## 📁 Key Files

### `src/app/page.tsx`
Home page with search functionality

### `src/lib/api.ts`
API client for communicating with backend

```typescript
export async function searchProducts(query: string) {
  const res = await fetch(`${API_URL}/api/search?q=${query}`);
  return res.json();
}
```

### `src/types/index.ts`
Shared TypeScript interfaces

```typescript
export interface Product {
  id: string;
  title: string;
  price: number;
  retailer: string;
  url: string;
  imageUrl?: string;
}
```

## 🎨 UI/UX Guidelines

### Design Principles
- **Speed First:** Optimistic UI updates
- **Mobile Responsive:** Mobile-first approach
- **Accessible:** WCAG 2.1 AA compliance
- **Clean:** Minimal, focused interface

### Component Standards
- Use TypeScript for all components
- Implement proper loading states
- Handle errors gracefully
- Follow Next.js best practices (Server Components where possible)

## 🧪 Testing

```bash
# Unit tests (planned)
npm test

# E2E tests (planned)
npm run test:e2e
```

## 📊 Performance Targets

- **LCP:** < 2.5s
- **FID:** < 100ms
- **CLS:** < 0.1
- **TTI:** < 3.5s

## 🔗 API Integration

### Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### API Endpoints Used

- `POST /api/scrape` - Trigger new scrape job
  - **Payload:** `{query: string, retailer: "amazon" | "flipkart"}`
  - **Required:** Both `query` and `retailer` fields
- `GET /api/products?query={query}` - Fetch products
- `GET /health` - Health check

### Example API Call

```typescript
// src/lib/api.ts
export async function triggerScrape(query: string, retailer: string) {
  const res = await fetch(`${API_URL}/api/scrape`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, retailer })
  });
  return res.json();
}
```

---

## 🔄 Backend Integration Notes

### Architecture Overview

```
Client (Next.js)
       ↓
    API Layer (Express)
       ↓
   Redis Queue ────→ Worker (Python)
       ↑                  ↓
       └──────────────MongoDB
```

**Key Principle:** Client **never** communicates directly with scraper worker.

### Async Scraping Pattern

The backend uses a **queue-driven architecture**, which means:

1. **Client triggers scrape job:**
   ```typescript
   POST /api/scrape { query: "iphone 15", retailer: "amazon" }
   → API responds immediately: { jobId: "123", message: "Job queued" }
   ```

2. **Job is queued (not executed immediately):**
   - API publishes job to Redis queue
   - Returns instantly (~10ms response)
   - Worker picks up job asynchronously

3. **Worker processes in background:**
   - Worker consumes job from queue
   - Scrapes retailer site (10-30 seconds)
   - Saves results to MongoDB

4. **Client fetches results:**
   ```typescript
   GET /api/products?query=iphone+15
   → Returns cached results from MongoDB
   ```

### Eventual Consistency

**Important:** Results are **eventually consistent**, not immediate.

```typescript
// Timeline:
0s   → User searches "iphone 15" for Amazon
0s   → Client calls POST /api/scrape
0.01s → API responds "Job queued"
0.02s → Client calls GET /api/products?query=iphone+15
0.03s → API returns [] (empty - worker hasn't finished yet)
15s  → Worker completes scraping
15s  → Results saved to MongoDB
20s  → User clicks "Refresh" or waits
20s  → Client calls GET /api/products again
20s  → API returns [products] (now available)
```

**Why This Matters:**
- ⚠️ First search may return empty results
- ⚠️ User needs to wait or refresh
- ⚠️ Not ideal UX, but architecturally superior

### Future Enhancement (Phase 2)

**Problem:** User doesn't know if worker is processing or finished.

**Solution:** Implement job status polling

```typescript
// Proposed implementation
async function searchWithPolling(query: string, retailer: string) {
  // 1. Trigger scrape
  const { jobId } = await triggerScrape(query, retailer);
  
  // 2. Show loading state
  setLoading(true);
  setMessage("Scraping Amazon for iPhones...");
  
  // 3. Poll for results
  const interval = setInterval(async () => {
    const products = await fetchProducts(query);
    
    if (products.length > 0) {
      setProducts(products);
      setLoading(false);
      clearInterval(interval);
    }
  }, 2000); // Check every 2 seconds
  
  // 4. Timeout after 60 seconds
  setTimeout(() => {
    clearInterval(interval);
    setLoading(false);
    setError("Scraping is taking longer than expected");
  }, 60000);
}
```

**Phase 2 TODO:**
- [ ] Add job status endpoint: `GET /api/jobs/:jobId`
- [ ] Implement polling logic in client
- [ ] Add loading skeletons
- [ ] Show estimated time remaining
- [ ] Add "Still working..." messages

### Why Not WebSockets?

**Considered:** Real-time updates via WebSockets

**Decision:** Polling is simpler for Phase 2

**Reasons:**
- Polling is stateless (easier to scale)
- WebSockets add complexity (connection management)
- Not needed for 2-second intervals
- Can optimize in Phase 3 if needed

### Cached Results Behavior

**Scenario 1: First Search (Cold)**
```
User: "iphone 15" on Amazon
→ POST /api/scrape (job queued)
→ GET /api/products (returns [])
→ Show: "Searching Amazon, please wait..."
→ Poll every 2s until results appear
```

**Scenario 2: Repeated Search (Warm)**
```
User: "iphone 15" on Amazon (someone searched before)
→ GET /api/products (returns cached results from MongoDB)
→ Show: Products immediately
→ Optionally: Trigger background refresh
```

**Cache Invalidation (Phase 3):**
- Results older than 24 hours considered stale
- Auto-refresh in background
- Show "Last updated: 2 hours ago"

### Error Handling

**Client should handle:**

1. **API Unavailable**
   ```typescript
   catch (error) {
     if (error.name === 'NetworkError') {
       showError("Cannot connect to server");
     }
   }
   ```

2. **Invalid Retailer**
   ```typescript
   if (response.status === 400) {
     showError("Unsupported retailer");
   }
   ```

3. **Empty Results After Timeout**
   ```typescript
   if (products.length === 0 && timeout) {
     showError("No products found");
   }
   ```

4. **Worker Failure** (Phase 3)
   - Check job status
   - Retry logic
   - Show "Something went wrong, try again"

### Benefits of This Architecture

✅ **Scalability**
- API and workers scale independently
- Multiple users can trigger jobs simultaneously
- Queue buffers load spikes

✅ **Reliability**
- Jobs don't fail if client disconnects
- Can retry failed jobs
- MongoDB caches results

✅ **Performance**
- Client gets instant response
- No timeout issues
- Background processing doesn't block UI

⚠️ **Trade-off:** Slightly worse UX initially (wait time), but vastly better architecture.

---

## 📦 Dependencies

### Core
- `next` - React framework
- `react` - UI library
- `typescript` - Type safety

### Planned
- `tailwindcss` - Styling (Phase 2)
- `gsap` - Animations (Phase 3)
- `recharts` - Price charts (Phase 3)
- `zustand` - State management (Phase 3)

## 🗺️ Roadmap

### Phase 2 Tasks
- [ ] Implement SearchBar component
- [ ] Create ProductCard component  
- [ ] Build product listing page
- [ ] Add loading skeletons
- [ ] Connect to API service
- [ ] Implement error boundaries
- [ ] **Add job status polling** (handle async scraping)
- [ ] **Show "Scraping in progress" states**
- [ ] **Implement result refresh logic**

### Phase 3 Tasks  
- [ ] Add Tailwind CSS
- [ ] Implement GSAP animations
- [ ] Create FilterPanel component
- [ ] Add price history visualization
- [ ] Optimize bundle size
- [ ] Add PWA support
- [ ] Implement infinite scroll
- [ ] Add dark mode
- [ ] **WebSocket integration for real-time updates** (optional)
- [ ] **Cache invalidation with staleness indicators**

## 📝 Change Log

### 2026-02-13 (Evening) - Backend Architecture Documentation
- Added "Backend Integration Notes" section
- Documented async scraping pattern and eventual consistency
- Explained queue-driven architecture implications for UX
- Added timeline diagram showing job processing flow
- Proposed job status polling implementation for Phase 2
- Documented cached results behavior (cold vs warm searches)
- Added error handling guidelines for async operations
- Updated Phase 2 roadmap with polling-related tasks
- Explained why client never calls scraper directly

### 2026-02-13 (Afternoon) - API Integration Update
- **[BREAKING]** Updated API integration to include `retailer` field
- Added example API call with new payload structure
- Documented required retailer field in scrape endpoint
- Added TypeScript example for triggerScrape function

### 2026-02-13 (Morning) - Documentation Enhancement
- Enhanced documentation
- Added comprehensive service overview
- Documented phases and roadmap

### 2026-02-11
- Next.js scaffold created
- TypeScript configured
- Basic project structure established

---

**Status:** 🟡 Phase 1 - Foundation Complete

[← Back to Main README](../README.md)

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
- `GET /api/products?query={query}` - Fetch products
- `GET /health` - Health check

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

### Phase 3 Tasks  
- [ ] Add Tailwind CSS
- [ ] Implement GSAP animations
- [ ] Create FilterPanel component
- [ ] Add price history visualization
- [ ] Optimize bundle size
- [ ] Add PWA support
- [ ] Implement infinite scroll
- [ ] Add dark mode

## 📝 Change Log

### 2026-02-13
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

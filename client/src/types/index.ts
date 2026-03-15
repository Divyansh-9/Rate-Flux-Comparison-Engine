export interface Product {
  id: string;
  name: string;
  description: string;
  imageUrl: string;
  category: string;
  createdAt: string;
  updatedAt: string;
}

export interface PriceEntry {
  id: string;
  productId: string;
  retailer: string;
  price: number;
  currency: string;
  url: string;
  scrapedAt: string;
}

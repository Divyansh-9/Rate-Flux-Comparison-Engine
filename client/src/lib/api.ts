export interface Product {
  _id: string;
  title: string;
  price: string;
  originalPrice?: string;
  source: "amazon" | "flipkart";
  url: string;
  image: string;
  rating?: string;
  reviews?: string;
  availability?: string;
  createdAt: string;
  updatedAt: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

export async function searchProducts(query: string): Promise<Product[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/products/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.message || "Failed to search products");
    }
    return res.json();
  } catch (error) {
    console.error("[api] searchProducts error:", error);
    throw error;
  }
}

export async function scrapeProducts(query: string, retailer: "amazon" | "flipkart"): Promise<void> {
  try {
    const res = await fetch(`${API_BASE_URL}/scrape`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, retailer }),
    });
    
    if (!res.ok) {
        throw new Error("Failed to enqueue scrape job");
    }
  } catch (error) {
    console.error("[api] scrapeProducts error:", error);
    throw error;
  }
}

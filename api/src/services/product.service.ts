import Product from "../models/product.model";
import { getCache, setCache } from "../lib/redis";

const CACHE_TTL_SECONDS = 300; // 5 minutes

export const findAll = async () => {
  return await Product.find().sort({ updatedAt: -1 });
};

export const findById = async (id: string) => {
  try {
    const cacheKey = `cache:product:${id}`;
    const cached = await getCache(cacheKey);
    if (cached) return cached;

    const product = await Product.findById(id);
    if (product) await setCache(cacheKey, product, CACHE_TTL_SECONDS);
    return product;
  } catch (error) {
    return null;
  }
};

export const search = async (query: string) => {
  const cacheKey = `cache:search:${query.toLowerCase()}`;
  
  // 1. Check Redis Cache
  const cachedResults = await getCache(cacheKey);
  if (cachedResults) {
    console.log(`[cache:hit] ${cacheKey}`);
    return cachedResults;
  }

  // 2. Cache Miss: Query MongoDB
  console.log(`[cache:miss] ${cacheKey}`);
  const results = await Product.find({ title: { $regex: query, $options: "i" } }).sort({
    updatedAt: -1,
  });

  // 3. Populate Cache
  await setCache(cacheKey, results, CACHE_TTL_SECONDS);
  
  return results;
};

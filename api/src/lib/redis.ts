import Redis from "ioredis";
import config from "../config";



let redis: Redis | undefined;

export function getRedis(): Redis {
  if (!redis) {
    redis = new Redis(config.redisUrl);
    redis.on("connect", () => console.log("[redis] connected"));
    redis.on("error", (err: Error) => console.error("[redis] error", err.message));
  }
  return redis;
}

const SCRAPE_QUEUE = "scrape:jobs";

export async function enqueueScrapeJob(payload: {
  query: string;
  retailer: string;
}): Promise<void> {
  const client = getRedis();
  await client.lpush(SCRAPE_QUEUE, JSON.stringify(payload));
}

// ── Caching Helpers ──

/**
 * Gets a cached JSON value from Redis
 */
export async function getCache<T>(key: string): Promise<T | null> {
  const client = getRedis();
  const data = await client.get(key);
  if (!data) return null;
  
  try {
    return JSON.parse(data) as T;
  } catch (error) {
    console.warn(`[redis] failed to parse cache for key ${key}`);
    return null;
  }
}

/**
 * Sets a JSON value in Redis with an optional expiration time in seconds (default: 300s / 5m)
 */
export async function setCache(
  key: string,
  value: unknown,
  expiresInSeconds: number = 300
): Promise<void> {
  const client = getRedis();
  const serialized = JSON.stringify(value);
  await client.set(key, serialized, "EX", expiresInSeconds);
}

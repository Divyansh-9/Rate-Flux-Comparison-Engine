import Redis from "ioredis";
import config from "../config";

interface ScrapeJobPayload {
  query: string;
  createdAt: string;
}

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

export async function enqueueScrapeJob(query: string): Promise<void> {
  const payload = JSON.stringify({ query, createdAt: new Date().toISOString() } as ScrapeJobPayload);
  await getRedis().lpush(SCRAPE_QUEUE, payload);
}

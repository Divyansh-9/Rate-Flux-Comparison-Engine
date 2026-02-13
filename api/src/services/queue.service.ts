import Redis from "ioredis";
import config from "../config";

let redis: Redis | null = null;

const getRedis = (): Redis => {
    if (!redis) {
        redis = new Redis(config.redisUrl);
        console.log("[Queue Service] Connected to Redis");
    }
    return redis;
};

export const publishScrapeJob = async (query: string): Promise<void> => {
    const redisClient = getRedis();
    const payload = JSON.stringify({ query });
    await redisClient.lpush("scrape:jobs", payload);
    console.log(`[Queue Service] Published scrape job for query: ${query}`);
};

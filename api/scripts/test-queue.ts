import { publishScrapeJob } from "../src/services/queue.service";
import Redis from "ioredis";
import config from "../src/config";

const testQueue = async () => {
    console.log("Testing publishScrapeJob...");

    const query = "test-query-" + Date.now();
    await publishScrapeJob(query);

    console.log("Verifying in Redis...");
    const redis = new Redis(config.redisUrl);
    const result = await redis.lpop("scrape:jobs");

    if (result) {
        const payload = JSON.parse(result);
        if (payload.query === query) {
            console.log("SUCCESS: Payload matched!");
        } else {
            console.error("FAILURE: Payload mismatch", payload);
        }
    } else {
        console.error("FAILURE: No item found in queue");
    }

    redis.disconnect();
    // We need to disconnect the service's redis client too, but it's not exported. 
    // For a script, process.exit is fine.
    process.exit(0);
};

testQueue().catch(err => {
    console.error(err);
    process.exit(1);
});

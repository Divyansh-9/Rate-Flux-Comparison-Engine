import { Router, Request, Response, NextFunction } from "express";
import { z } from "zod";
import { enqueueScrapeJob } from "../lib/redis";

export const scrapeRouter = Router();

const scrapeSchema = z.object({
  query: z.string().min(1).max(200),
  retailer: z.enum(["amazon", "flipkart"]),
});

scrapeRouter.post("/", async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { query, retailer } = scrapeSchema.parse(req.body);
    await enqueueScrapeJob(query, retailer);
    res.status(202).json({ message: "Scrape job queued", query, retailer });
  } catch (err) {
    next(err);
  }
});

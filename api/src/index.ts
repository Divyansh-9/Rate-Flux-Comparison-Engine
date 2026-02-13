import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import config from "./config";
import { errorHandler } from "./middleware/errorHandler";
import { productRouter } from "./routes/product.routes";
import { scrapeRouter } from "./routes/scrape.routes";
import { healthRouter } from "./routes/health.routes";
import { connectDB } from "./config/db";
import { getRedis } from "./lib/redis";

const app = express();

// ── Global Middleware ──
app.use(helmet());
app.use(cors({ origin: config.corsOrigin }));
app.use(express.json());
app.use(morgan("dev"));

// ── Routes ──
app.use("/api/health", healthRouter);
app.use("/api/products", productRouter);
app.use("/api/scrape", scrapeRouter);

// ── Error Handling ──
app.use(errorHandler);

async function bootstrap() {
  await connectDB();
  getRedis(); // warm the connection
  app.listen(config.port, () => {
    console.log(`[api] running on port ${config.port} (${config.nodeEnv})`);
  });
}

bootstrap().catch((err) => {
  console.error("[api] failed to start", err);
  process.exit(1);
});

export default app;

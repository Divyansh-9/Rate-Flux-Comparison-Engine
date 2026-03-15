import { Request, Response, NextFunction } from "express";
import { z } from "zod";

// ── Schemas ──

export const searchSchema = z.object({
  query: z.object({
    q: z.string({
      required_error: "Missing query parameter ?q=",
    }).min(1, "Search query must not be empty"),
  }),
});

// ── Middleware ──

export const validateSearchQuery = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // Note: req.query is passed directly to the schema
    searchSchema.parse({
      query: req.query,
    });
    next();
  } catch (error) {
    if (error instanceof z.ZodError) {
       res.status(400).json({
        message: "Invalid query parameters",
        errors: error.errors.map((e) => ({
          path: e.path.join("."),
          message: e.message,
        })),
      });
      return;
    }
    next(error);
  }
};

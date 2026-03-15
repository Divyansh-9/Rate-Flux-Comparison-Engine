import { Router } from "express";
import {
  getAllProducts,
  getProductById,
  searchProducts,
} from "../controllers/product.controller";
import { validateSearchQuery } from "../middleware/product.validator";

export const productRouter = Router();

productRouter.get("/", getAllProducts);
productRouter.get("/search", validateSearchQuery, searchProducts);
productRouter.get("/:id", getProductById);

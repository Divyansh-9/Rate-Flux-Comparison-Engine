import { Router } from "express";
import {
  getAllProducts,
  getProductById,
  searchProducts,
} from "../controllers/product.controller";

export const productRouter = Router();

productRouter.get("/", getAllProducts);
productRouter.get("/search", searchProducts);
productRouter.get("/:id", getProductById);

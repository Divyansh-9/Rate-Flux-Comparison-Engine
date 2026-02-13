import { Request, Response, NextFunction } from "express";
import * as productService from "../services/product.service";

export async function getAllProducts(
  _req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const products = await productService.findAll();
    res.json(products);
  } catch (err) {
    next(err);
  }
}

export async function getProductById(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const product = await productService.findById(req.params.id);
    if (!product) {
      res.status(404).json({ message: "Product not found" });
      return;
    }
    res.json(product);
  } catch (err) {
    next(err);
  }
}

export async function searchProducts(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const query = (req.query.q as string) ?? "";
    if (!query) {
      res.status(400).json({ message: "Missing query parameter ?q=" });
      return;
    }
    const products = await productService.search(query);
    res.json(products);
  } catch (err) {
    next(err);
  }
}

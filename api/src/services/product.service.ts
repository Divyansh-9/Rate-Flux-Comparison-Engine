import Product from "../models/product.model";

export const findAll = async () => {
  return await Product.find().sort({ updatedAt: -1 });
};

export const findById = async (id: string) => {
  try {
    return await Product.findById(id);
  } catch (error) {
    return null;
  }
};

export const search = async (query: string) => {
  return await Product.find({ title: { $regex: query, $options: "i" } }).sort({
    updatedAt: -1,
  });
};

import mongoose, { Document, Schema } from "mongoose";

export interface IProduct extends Document {
  title: string;
  price: number;
  source: string;
  url: string;
  image: string;
  query: string;
  createdAt: Date;
  updatedAt: Date;
}

const ProductSchema: Schema = new Schema(
  {
    title: { type: String, required: true },
    price: { type: Number, required: true },
    source: { type: String, required: true },
    url: { type: String, required: true, unique: true },
    image: { type: String },
    query: { type: String },
  },
  {
    timestamps: true,
  }
);

export default mongoose.model<IProduct>("Product", ProductSchema);

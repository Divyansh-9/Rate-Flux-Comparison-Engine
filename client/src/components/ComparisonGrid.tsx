"use client";

import { ExternalLink, ShoppingCart, RefreshCcw } from "lucide-react";
import type { Product } from "../lib/api";

interface ComparisonGridProps {
  products: Product[];
  onRefreshScrape?: (retailer: string) => void;
  isLoadingTarget?: string | null;
}

export function ComparisonGrid({ products, onRefreshScrape, isLoadingTarget }: ComparisonGridProps) {
  // Group products by source
  const amazonProducts = products.filter((p) => p.source === "amazon");
  const flipkartProducts = products.filter((p) => p.source === "flipkart");

  return (
    <div aria-label="Product Comparison Grid" className="w-full max-w-6xl mx-auto space-y-8 animate-fade-in relative z-20">
      
      {/* Header / Stats */}
      <div className="flex items-center justify-between bg-white/5 border border-white/10 p-4 rounded-xl backdrop-blur-md">
        <h2 className="text-xl font-bold text-white">Comparison Results</h2>
        <div className="flex gap-4">
          <span className="text-sm font-medium text-cta px-3 py-1 bg-cta/10 rounded-full border border-cta/20">
            {amazonProducts.length} Amazon items
          </span>
          <span className="text-sm font-medium text-blue-400 px-3 py-1 bg-blue-500/10 rounded-full border border-blue-500/20">
            {flipkartProducts.length} Flipkart items
          </span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 items-start">
        {/* Amazon Column */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/10">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <ShoppingCart className="w-6 h-6 text-cta" /> Amazon
            </h3>
             {onRefreshScrape && (
               <button 
                onClick={() => onRefreshScrape("amazon")}
                disabled={isLoadingTarget === 'amazon'}
                className="text-gray-400 hover:text-cta transition-colors p-2"
                title="Force Scrape Amazon"
               >
                 <RefreshCcw className={`w-4 h-4 ${isLoadingTarget === 'amazon' ? 'animate-spin text-cta' : ''}`} />
               </button>
            )}
          </div>
          {amazonProducts.length > 0 ? (
            amazonProducts.map((p) => <ProductCard key={p._id} product={p} brandColor="border-cta/30" hoverColor="hover:border-cta" />)
          ) : (
            <EmptyState retailer="Amazon" />
          )}
        </div>

        {/* Flipkart Column */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/10">
            <h3 className="text-2xl font-bold text-white flex items-center gap-2">
              <ShoppingCart className="w-6 h-6 text-blue-400" /> Flipkart
            </h3>
             {onRefreshScrape && (
               <button 
                onClick={() => onRefreshScrape("flipkart")}
                disabled={isLoadingTarget === 'flipkart'}
                className="text-gray-400 hover:text-blue-400 transition-colors p-2"
                title="Force Scrape Flipkart"
               >
                 <RefreshCcw className={`w-4 h-4 ${isLoadingTarget === 'flipkart' ? 'animate-spin text-blue-400' : ''}`} />
               </button>
            )}
          </div>
          {flipkartProducts.length > 0 ? (
            flipkartProducts.map((p) => <ProductCard key={p._id} product={p} brandColor="border-blue-500/30" hoverColor="hover:border-blue-400" />)
          ) : (
            <EmptyState retailer="Flipkart" />
          )}
        </div>
      </div>
    </div>
  );
}

function ProductCard({ product, brandColor, hoverColor }: { product: Product, brandColor: string, hoverColor: string }) {
  return (
    <div className={`card text-left p-4 flex gap-4 ${brandColor} ${hoverColor} transition-colors group`}>
      <div className="w-24 h-24 shrink-0 bg-white rounded-md flex items-center justify-center overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={product.image} alt={product.title} className="w-full h-full object-contain mix-blend-multiply" />
      </div>
      <div className="flex flex-col justify-between flex-1 min-w-0">
        <div>
          <h4 className="font-medium text-gray-200 truncate group-hover:text-white transition-colors" title={product.title}>
            {product.title}
          </h4>
          <div className="flex items-end gap-2 mt-1">
            <span className="text-2xl font-bold text-white">{product.price}</span>
            {product.originalPrice && (
              <span className="text-sm text-gray-500 line-through mb-1">{product.originalPrice}</span>
            )}
          </div>
        </div>
        
        <div className="flex items-center justify-between mt-3">
            <div className="text-xs text-gray-400">
                {product.rating && <span className="mr-2">★ {product.rating}</span>}
                {product.availability && <span className="text-green-400">{product.availability}</span>}
            </div>
            <a 
                href={product.url} 
                target="_blank" 
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-sm font-medium text-gray-300 hover:text-white transition-colors p-2 bg-white/5 rounded-md hover:bg-white/10"
            >
                View <ExternalLink className="w-4 h-4" />
            </a>
        </div>
      </div>
    </div>
  );
}

function EmptyState({ retailer }: { retailer: string }) {
  return (
    <div className="p-8 text-center border border-dashed border-white/10 rounded-xl bg-white/5 backdrop-blur-sm">
      <p className="text-gray-400">No {retailer} results found directly matching this cached query.</p>
      <p className="text-sm mt-2 text-gray-500">Hit the refresh icon above to send a background scrape job.</p>
    </div>
  );
}

"use client";

import { useState } from "react";
import { SearchInput } from "../components/SearchInput";
import { ComparisonGrid } from "../components/ComparisonGrid";
import { searchProducts, scrapeProducts, Product } from "../lib/api";
import { Zap, ShieldCheck, BarChart3, AlertCircle } from "lucide-react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // State for specific retailer force-refreshes
  const [isLoadingTarget, setIsLoadingTarget] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      const results = await searchProducts(query);
      setProducts(results);
      setHasSearched(true);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to fetch comparisons.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleForceScrape = async (retailer: "amazon" | "flipkart") => {
    setIsLoadingTarget(retailer);
    try {
      await scrapeProducts(query, retailer);
      // Wait a few seconds to let the Python scraper populate Mongo via ScraperAPI
      setTimeout(async () => {
         const results = await searchProducts(query);
         setProducts(results);
         setIsLoadingTarget(null);
      }, 5000);
    } catch (err) {
      console.error(err);
      setIsLoadingTarget(null);
    }
  };

  return (
    <main aria-label="Home page" className="flex flex-col items-center justify-center min-h-screen p-8 text-center bg-transparent z-10 relative">
      <div className="w-full max-w-6xl mx-auto space-y-12 mt-16">
        
        {/* Header Section */}
        <section className={`space-y-6 transition-all duration-700 ${hasSearched ? '-mt-8 mb-8 scale-95' : 'mt-16 animate-fade-in'}`}>
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm font-medium text-cta/80 backdrop-blur-sm mb-4">
            <Zap className="w-4 h-4" /> Ultra-Fast Redis Cache Engine
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white !leading-tight">
            Compare premium <br /> <span className="text-transparent bg-clip-text bg-gradient-to-r from-cta to-yellow-200">products globally.</span>
          </h1>
          {!hasSearched && (
            <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto animate-fade-in" style={{ animationDelay: '200ms' }}>
              Rate Flux Engine bypasses proactive bot detection to aggregate accurate pricing data from Amazon and Flipkart directly to your dashboard.
            </p>
          )}
        </section>

        {/* Dynamic Search Area */}
        <section className={`w-full relative z-30 transition-all duration-500`}>
            {error && (
              <div className="flex items-center justify-center gap-2 text-red-400 bg-red-500/10 border border-red-500/20 p-4 rounded-xl max-w-2xl mx-auto mb-6">
                <AlertCircle className="w-5 h-5 shrink-0" /> {error}
              </div>
            )}
            <SearchInput 
              query={query} 
              setQuery={setQuery} 
              onSearch={handleSearch} 
              isLoading={isLoading} 
            />
        </section>

        {/* Contextual Body */}
        {hasSearched ? (
           <ComparisonGrid 
              products={products} 
              onRefreshScrape={(retailer) => handleForceScrape(retailer as "amazon"|"flipkart")} 
              isLoadingTarget={isLoadingTarget} 
           />
        ) : (
          <section className="grid md:grid-cols-3 gap-6 pt-16 max-w-5xl mx-auto animate-fade-in" style={{ animationDelay: '400ms' }}>
            <FeatureCard 
              icon={<ShieldCheck className="w-8 h-8 text-cta" />} 
              title="Bot-Bypass Proxy" 
              desc="ScraperAPI integration guarantees seamless data extraction across the web." 
            />
            <FeatureCard 
              icon={<Zap className="w-8 h-8 text-cta" />} 
              title="Redis Caching" 
              desc="Responses are lightning-fast with Cache-Aside TTL memory logic." 
            />
            <FeatureCard 
              icon={<BarChart3 className="w-8 h-8 text-cta" />} 
              title="Zod Validation" 
              desc="Strict proxy payload rules ensure application state stability." 
            />
          </section>
        )}

      </div>
    </main>
  );
}

function FeatureCard({ icon, title, desc }: { icon: React.ReactNode; title: string; desc: string }) {
  return (
    <div className="card text-left space-y-4 hover:border-cta/50 transition-colors">
      <div className="p-3 bg-white/5 inline-flex rounded-lg border border-white/10">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white">{title}</h3>
      <p className="text-gray-400 leading-relaxed">{desc}</p>
    </div>
  );
}

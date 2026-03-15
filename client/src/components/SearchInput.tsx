"use client";

import { Search, Loader2 } from "lucide-react";

interface SearchInputProps {
  query: string;
  setQuery: (val: string) => void;
  onSearch: () => void;
  isLoading?: boolean;
}

export function SearchInput({ query, setQuery, onSearch, isLoading }: SearchInputProps) {
  return (
    <div className="relative w-full max-w-2xl mx-auto group">
      {/* Ambient background glow for the input container */}
      <div className="absolute -inset-1 bg-gradient-to-r from-cta/30 to-white/10 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-500"></div>
      
      <div className="relative flex items-center bg-white/5 border border-white/10 rounded-xl p-2 backdrop-blur-md shadow-xl transition-all duration-300 group-hover:bg-white/10">
        <Search className="w-6 h-6 text-gray-400 ml-3 shrink-0" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && onSearch()}
          placeholder="Search for a product... (e.g., iPhone 15 Pro)"
          className="flex-1 bg-transparent border-none text-white px-4 py-3 outline-none placeholder:text-gray-500 text-lg"
          disabled={isLoading}
        />
        <button
          onClick={onSearch}
          disabled={isLoading || !query.trim()}
          className="bg-cta text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200 cursor-pointer hover:bg-cta/90 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Searching
            </>
          ) : (
            "Compare Prices"
          )}
        </button>
      </div>
    </div>
  );
}

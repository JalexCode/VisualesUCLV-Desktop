import React, { useState, useEffect } from 'react';
import { Search, Command } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore } from '../store/useStore';
import { searchService } from '../lib/search';
import type { FlatNode } from '../types';

export const SearchOverlay: React.FC<{ flatData: FlatNode[] }> = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const { setCurrentPath } = useStore();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setIsOpen((open) => !open);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  useEffect(() => {
    if (query.length > 1) {
      const searchResults = searchService.search(query);
      setResults(searchResults.slice(0, 8));
    } else {
      setResults([]);
    }
  }, [query]);

  const handleSelect = (path: string) => {
    setCurrentPath(path);
    setIsOpen(false);
    setQuery('');
  };

  return (
    <>
      <div
        onClick={() => setIsOpen(true)}
        className="flex items-center space-x-2 px-3 py-1.5 rounded-md bg-accent/50 text-muted-foreground border border-border cursor-pointer hover:bg-accent transition-colors w-64"
      >
        <Search size={14} />
        <span className="text-sm flex-1">Search files...</span>
        <div className="flex items-center space-x-1 border rounded px-1 bg-background text-[10px]">
          <Command size={10} />
          <span>K</span>
        </div>
      </div>

      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="absolute inset-0 bg-background/80 backdrop-blur-sm"
            />
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="relative w-full max-w-xl bg-card border border-border shadow-2xl rounded-xl overflow-hidden"
            >
              <div className="flex items-center p-4 border-b">
                <Search className="mr-3 text-muted-foreground" size={20} />
                <input
                  autoFocus
                  className="flex-1 bg-transparent border-none outline-none text-lg placeholder:text-muted-foreground"
                  placeholder="Type to search..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
              </div>
              <div className="max-h-[60vh] overflow-y-auto">
                {results.length > 0 ? (
                  <div className="p-2">
                    {results.map((result) => (
                      <div
                        key={result.item.path}
                        className="flex flex-col p-3 rounded-lg hover:bg-accent cursor-pointer group"
                        onClick={() => handleSelect(result.item.path)}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-medium text-foreground">{result.item.name}</span>
                          <span className="text-[10px] text-muted-foreground bg-accent px-1.5 py-0.5 rounded uppercase">
                            {result.item.type}
                          </span>
                        </div>
                        <span className="text-xs text-muted-foreground truncate">{result.item.path}</span>
                      </div>
                    ))}
                  </div>
                ) : query.length > 1 ? (
                  <div className="p-8 text-center text-muted-foreground">No results found.</div>
                ) : (
                  <div className="p-8 text-center text-muted-foreground">Start typing to search...</div>
                )}
              </div>
              <div className="p-3 border-t bg-muted/30 flex items-center justify-between text-[10px] text-muted-foreground">
                <div className="flex items-center space-x-3">
                  <span className="flex items-center">
                    <span className="border rounded px-1 mr-1">↵</span> Select
                  </span>
                  <span className="flex items-center">
                    <span className="border rounded px-1 mr-1">↑↓</span> Navigate
                  </span>
                </div>
                <span>Visuales UCLV Search</span>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
};

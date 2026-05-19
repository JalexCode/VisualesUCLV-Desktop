import { useMemo, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Breadcrumbs, FileList } from './components/MainContent';
import { SearchOverlay } from './components/SearchOverlay';
import { mockData } from './mockData';
import { useStore } from './store/useStore';
import { flattenTree } from './lib/treeUtils';
import { searchService } from './lib/search';
import type { FolderNode, RepoNode } from './types';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const { currentPath } = useStore();

  const flatData = useMemo(() => flattenTree(mockData), []);

  useEffect(() => {
    searchService.init(flatData);
  }, [flatData]);

  const currentFolder = useMemo(() => {
    const findNode = (node: RepoNode, path: string): RepoNode | null => {
      if (node.path === path) return node;
      if ('isFolder' in node && node.children) {
        for (const child of node.children) {
          const found = findNode(child, path);
          if (found) return found;
        }
      }
      return null;
    };

    const node = findNode(mockData, currentPath);
    if (node && 'isFolder' in node) {
      return node as FolderNode;
    }

    // If it's a file, find its parent folder
    if (node && !('isFolder' in node)) {
      const parentPath = currentPath.substring(0, currentPath.lastIndexOf('/', currentPath.length - 2) + 1);
      const parent = findNode(mockData, parentPath);
      if (parent && 'isFolder' in parent) {
        return parent as FolderNode;
      }
    }

    return mockData;
  }, [currentPath]);

  return (
    <div className="flex h-screen bg-background overflow-hidden font-sans antialiased text-foreground">
      <Sidebar data={mockData} />

      <main className="flex-1 flex flex-col min-w-0">
        <header className="h-16 border-b flex items-center justify-between px-6 bg-card/50 backdrop-blur-md sticky top-0 z-10">
          <div className="flex-1 min-w-0">
             <h2 className="text-sm font-medium text-muted-foreground truncate">
                {currentPath === '/' ? 'Home' : currentPath.split('/').filter(Boolean).pop()}
             </h2>
          </div>
          <SearchOverlay flatData={flatData} />
        </header>

        <div className="flex-1 p-6 flex flex-col overflow-hidden">
          <Breadcrumbs />

          <AnimatePresence mode="wait">
            <motion.div
              key={currentFolder.path}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="flex-1 flex flex-col overflow-hidden"
            >
              <FileList currentFolder={currentFolder} />
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

export default App;

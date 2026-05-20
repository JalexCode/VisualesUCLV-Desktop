import { useMemo, useEffect, useCallback } from 'react';
import { Sidebar } from './components/Sidebar';
import { Breadcrumbs, FileList } from './components/MainContent';
import { SearchOverlay } from './components/SearchOverlay';
import { useStore } from './store/useStore';
import { flattenTree } from './lib/treeUtils';
import { searchService } from './lib/search';
import { parseListado, parseFolderPage, VISUALES_URL } from './lib/parser';
import { saveTree, loadTree } from './lib/storage';
import type { FolderNode, RepoNode } from './types';
import { motion, AnimatePresence } from 'framer-motion';
import { RefreshCcw, AlertCircle, Loader2 } from 'lucide-react';

function App() {
  const {
    tree, setTree, currentPath, updateFolderChildren,
    isLoading, setLoading, error, setError
  } = useStore();

  const flatData = useMemo(() => tree ? flattenTree(tree) : [], [tree]);

  useEffect(() => {
    if (flatData.length > 0) {
      searchService.init(flatData);
    }
  }, [flatData]);

  // Load tree from IndexedDB on startup
  useEffect(() => {
    async function init() {
      const savedTree = await loadTree();
      if (savedTree) {
        setTree(savedTree);
      }
    }
    init();
  }, [setTree]);

  const handleUpdateRepo = async () => {
    setLoading(true);
    setError(null);
    try {
      // In a real environment, we might hit a CORS issue if we fetch directly from the browser.
      // For this implementation, we assume the environment or a proxy allows the request.
      const response = await fetch(`${VISUALES_URL}/listado.html`);
      if (!response.ok) throw new Error('Failed to fetch listado.html');
      const html = await response.text();
      const newTree = parseListado(html);
      setTree(newTree);
      await saveTree(newTree);
    } catch (err: any) {
      setError(err.message || 'An error occurred while updating');
    } finally {
      setLoading(false);
    }
  };

  const loadFolderContent = useCallback(async (path: string) => {
    if (!tree) return;
    setLoading(true);
    try {
      const response = await fetch(`${VISUALES_URL}${path}`);
      if (!response.ok) throw new Error('Failed to fetch folder content');
      const html = await response.text();
      const files = parseFolderPage(html, path);
      updateFolderChildren(path, files);
      // Persist the updated tree
      const updatedTree = useStore.getState().tree;
      if (updatedTree) await saveTree(updatedTree);
    } catch (err: any) {
      setError(err.message || 'An error occurred while loading folder');
    } finally {
      setLoading(false);
    }
  }, [tree, updateFolderChildren, setLoading, setError]);

  const currentFolder = useMemo(() => {
    if (!tree) return null;
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

    const node = findNode(tree, currentPath);
    if (node && 'isFolder' in node) {
      const folder = node as FolderNode;
      // If folder has no files yet (only subfolders from listado.html), try loading them
      const hasFiles = folder.children?.some(c => !('isFolder' in c));
      if (!hasFiles && !isLoading) {
        loadFolderContent(currentPath);
      }
      return folder;
    }

    return tree;
  }, [tree, currentPath, loadFolderContent, isLoading]);

  return (
    <div className="flex h-screen bg-background overflow-hidden font-sans antialiased text-foreground">
      {tree ? (
        <>
          <Sidebar data={tree} />

          <main className="flex-1 flex flex-col min-w-0">
            <header className="h-16 border-b flex items-center justify-between px-6 bg-card/50 backdrop-blur-md sticky top-0 z-10">
              <div className="flex items-center space-x-4 min-w-0">
                <h2 className="text-sm font-medium text-muted-foreground truncate max-w-[200px]">
                  {currentPath === '/' ? 'Home' : currentPath.split('/').filter(Boolean).pop()}
                </h2>
                <button
                  onClick={handleUpdateRepo}
                  disabled={isLoading}
                  className="p-2 hover:bg-accent rounded-md transition-colors disabled:opacity-50"
                  title="Update Repository Tree"
                >
                  <RefreshCcw size={16} className={isLoading ? "animate-spin" : ""} />
                </button>
              </div>

              <div className="flex items-center space-x-4">
                {error && (
                  <div className="flex items-center text-destructive text-xs bg-destructive/10 px-2 py-1 rounded">
                    <AlertCircle size={14} className="mr-1" />
                    {error}
                  </div>
                )}
                <SearchOverlay flatData={flatData} />
              </div>
            </header>

            <div className="flex-1 p-6 flex flex-col overflow-hidden">
              <Breadcrumbs />

              <AnimatePresence mode="wait">
                <motion.div
                  key={currentPath}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className="flex-1 flex flex-col overflow-hidden"
                >
                  {currentFolder && <FileList currentFolder={currentFolder} />}
                </motion.div>
              </AnimatePresence>
            </div>

            <footer className="h-8 border-t bg-card/30 px-6 flex items-center justify-between text-[10px] text-muted-foreground">
              <div className="flex items-center space-x-4">
                <span>Total Items: {currentFolder?.children?.length || 0}</span>
                {currentFolder && (
                  <span>
                    Total Size: {currentFolder.children?.reduce((acc, c) => acc + ('size' in c ? c.size : 0), 0).toLocaleString()} bytes
                  </span>
                )}
              </div>
              <span>Visuales UCLV Explorer Web v1.0</span>
            </footer>
          </main>
        </>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="max-w-md"
          >
            <h1 className="text-4xl font-bold text-sky-500 mb-4">Visuales UCLV</h1>
            <p className="text-muted-foreground mb-8">
              Welcome to the modern web explorer for Visuales UCLV.
              To start browsing, we need to download the repository structure.
            </p>
            <button
              onClick={handleUpdateRepo}
              disabled={isLoading}
              className="px-8 py-3 bg-sky-500 hover:bg-sky-600 text-white rounded-full font-medium transition-all shadow-lg shadow-sky-500/20 flex items-center mx-auto space-x-2 disabled:opacity-50"
            >
              {isLoading ? <Loader2 className="animate-spin" /> : <RefreshCcw size={18} />}
              <span>{isLoading ? 'Downloading Tree...' : 'Initialize Repository'}</span>
            </button>
            {error && <p className="mt-4 text-destructive text-sm">{error}</p>}
          </motion.div>
        </div>
      )}
    </div>
  );
}

export default App;

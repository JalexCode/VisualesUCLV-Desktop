import { create } from 'zustand';
import type { RepoNode, FolderNode } from '../types';

interface AppState {
  tree: FolderNode | null;
  currentPath: string;
  expandedFolders: Set<string>;
  favorites: Set<string>;
  searchQuery: string;
  isSidebarOpen: boolean;
  selectedNode: RepoNode | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setTree: (tree: FolderNode) => void;
  setCurrentPath: (path: string) => void;
  toggleFolder: (path: string) => void;
  toggleFavorite: (path: string) => void;
  setSearchQuery: (query: string) => void;
  setSidebarOpen: (open: boolean) => void;
  setSelectedNode: (node: RepoNode | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updateFolderChildren: (path: string, children: RepoNode[]) => void;
}

export const useStore = create<AppState>((set) => ({
  tree: null,
  currentPath: '/',
  expandedFolders: new Set(['/']),
  favorites: new Set(),
  searchQuery: '',
  isSidebarOpen: true,
  selectedNode: null,
  isLoading: false,
  error: null,

  setTree: (tree) => set({ tree }),

  setCurrentPath: (path) => set({ currentPath: path }),

  toggleFolder: (path) => set((state) => {
    const newExpanded = new Set(state.expandedFolders);
    if (newExpanded.has(path)) {
      newExpanded.delete(path);
    } else {
      newExpanded.add(path);
    }
    return { expandedFolders: newExpanded };
  }),

  toggleFavorite: (path) => set((state) => {
    const newFavorites = new Set(state.favorites);
    if (newFavorites.has(path)) {
      newFavorites.delete(path);
    } else {
      newFavorites.add(path);
    }
    return { favorites: newFavorites };
  }),

  setSearchQuery: (query) => set({ searchQuery: query }),

  setSidebarOpen: (open) => set({ isSidebarOpen: open }),

  setSelectedNode: (node) => set({ selectedNode: node }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  updateFolderChildren: (path, children) => set((state) => {
    if (!state.tree) return state;

    const newTree = { ...state.tree };
    const updateNode = (node: FolderNode): boolean => {
      if (node.path === path) {
        node.children = [...(node.children?.filter(c => 'isFolder' in c) || []), ...children];
        return true;
      }
      if (node.children) {
        for (const child of node.children) {
          if ('isFolder' in child) {
            if (updateNode(child as FolderNode)) return true;
          }
        }
      }
      return false;
    };

    updateNode(newTree);
    return { tree: newTree };
  }),
}));

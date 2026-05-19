import { create } from 'zustand';
import type { RepoNode } from '../types';

interface AppState {
  currentPath: string;
  expandedFolders: Set<string>;
  favorites: Set<string>;
  searchQuery: string;
  isSidebarOpen: boolean;
  selectedNode: RepoNode | null;

  // Actions
  setCurrentPath: (path: string) => void;
  toggleFolder: (path: string) => void;
  toggleFavorite: (path: string) => void;
  setSearchQuery: (query: string) => void;
  setSidebarOpen: (open: boolean) => void;
  setSelectedNode: (node: RepoNode | null) => void;
}

export const useStore = create<AppState>((set) => ({
  currentPath: '/',
  expandedFolders: new Set(['/']),
  favorites: new Set(),
  searchQuery: '',
  isSidebarOpen: true,
  selectedNode: null,

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
}));

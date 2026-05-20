import Fuse from 'fuse.js';
import type { FlatNode } from '../types';

export class SearchService {
  private fuse: Fuse<FlatNode> | null = null;

  init(data: FlatNode[]) {
    this.fuse = new Fuse(data, {
      keys: ['name', 'path'],
      threshold: 0.3,
      includeMatches: true,
      useExtendedSearch: true,
    });
  }

  search(query: string) {
    if (!this.fuse) return [];
    return this.fuse.search(query);
  }
}

export const searchService = new SearchService();

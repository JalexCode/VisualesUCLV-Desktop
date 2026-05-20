import type { RepoNode, FlatNode } from '../types';

export function flattenTree(node: RepoNode, parentId: string | null = null): FlatNode[] {
  const current: FlatNode = {
    id: node.path,
    name: node.name,
    path: node.path,
    type: 'isFolder' in node ? 'folder' : node.type,
    parentId,
    size: 'size' in node ? node.size : undefined,
    modificationDate: 'modificationDate' in node ? node.modificationDate : undefined,
    url: 'url' in node ? node.url : undefined,
  };

  const results: FlatNode[] = [current];

  if ('isFolder' in node && node.children) {
    node.children.forEach(child => {
      results.push(...flattenTree(child, node.path));
    });
  }

  return results;
}

export function formatSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

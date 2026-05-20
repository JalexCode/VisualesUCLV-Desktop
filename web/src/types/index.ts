export type FileType = 'image' | 'video' | 'audio' | 'text' | 'archive' | 'unknown';

export interface FileNode {
  name: string;
  type: FileType;
  size: number;
  modificationDate: string;
  url: string;
  path: string;
}

export interface FolderNode {
  name: string;
  path: string;
  children?: (FileNode | FolderNode)[];
  isFolder: true;
}

export type RepoNode = FileNode | FolderNode;

export interface TreeData {
  root: FolderNode;
}

export interface FlatNode {
  name: string;
  path: string;
  type: FileType | 'folder';
  size?: number;
  modificationDate?: string;
  url?: string;
  parentId: string | null;
  id: string;
}

import type { FileNode, FolderNode, FileType } from '../types';

export const VISUALES_URL = 'http://visuales.uclv.cu';

export function parseListado(html: string): FolderNode {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  const links = doc.querySelectorAll('a');

  const root: FolderNode = {
    name: 'Visuales UCLV',
    path: '/',
    isFolder: true,
    children: []
  };

  const nodeMap = new Map<string, FolderNode>();
  nodeMap.set('/', root);

  links.forEach((link, index) => {
    if (index === 0) return; // Skip root link usually

    const href = link.getAttribute('href') || '';
    if (!href.endsWith('/')) return; // In listado.html, only directories are listed

    const decodedHref = decodeURIComponent(href);
    const path = decodedHref.startsWith('http') ? new URL(decodedHref).pathname : decodedHref;
    const parts = path.split('/').filter(Boolean);
    const name = link.textContent?.trim() || parts[parts.length - 1];

    const newNode: FolderNode = {
      name,
      path: path.endsWith('/') ? path : path + '/',
      isFolder: true,
      children: []
    };

    nodeMap.set(newNode.path, newNode);

    // Find parent
    const parentPath = path.substring(0, path.lastIndexOf('/', path.length - 2) + 1);
    const parentNode = nodeMap.get(parentPath || '/');
    if (parentNode) {
      parentNode.children = parentNode.children || [];
      parentNode.children.push(newNode);
    }
  });

  return root;
}

export function parseFolderPage(html: string, parentPath: string): FileNode[] {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  const rows = Array.from(doc.querySelectorAll('tr')).slice(3); // Skip headers and parent link
  const files: FileNode[] = [];

  rows.forEach(row => {
    const cols = row.querySelectorAll('td');
    if (cols.length < 5) return;

    const img = cols[0].querySelector('img');
    const link = cols[1].querySelector('a');
    if (!link) return;

    const name = link.textContent?.trim() || '';
    const href = link.getAttribute('href') || '';
    const dateStr = cols[2].textContent?.trim() || '';
    const sizeStr = cols[3].textContent?.trim() || '';

    if (sizeStr === '-') return; // It's a directory, we handle directories via listado.html

    const type = getFileTypeFromIcon(img?.getAttribute('src') || '');
    const size = parseSize(sizeStr);

    files.push({
      name,
      type,
      size,
      modificationDate: dateStr,
      url: VISUALES_URL + parentPath + href,
      path: parentPath + name
    });
  });

  return files;
}

function getFileTypeFromIcon(src: string): FileType {
  if (src.includes('movie') || src.includes('video')) return 'video';
  if (src.includes('image') || src.includes('picture')) return 'image';
  if (src.includes('audio')) return 'audio';
  if (src.includes('compressed') || src.includes('archive') || src.includes('rar') || src.includes('zip')) return 'archive';
  if (src.includes('text') || src.includes('doc')) return 'text';
  return 'unknown';
}

function parseSize(sizeStr: string): number {
  if (!sizeStr || sizeStr === '-') return 0;
  const num = parseFloat(sizeStr);
  if (sizeStr.includes('K')) return num * 1024;
  if (sizeStr.includes('M')) return num * 1024 * 1024;
  if (sizeStr.includes('G')) return num * 1024 * 1024 * 1024;
  return num;
}

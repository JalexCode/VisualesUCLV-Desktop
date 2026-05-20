import React from 'react';
import { useStore } from '../store/useStore';
import { ChevronRight, Home, Download, File, Image, Video, Music, FileText, Archive } from 'lucide-react';
import type { FolderNode } from '../types';
import { formatSize } from '../lib/treeUtils';
import { Table, TableHead, TableHeader, TableRow } from './ui/table';
import { Virtuoso } from 'react-virtuoso';

export const Breadcrumbs: React.FC = () => {
  const { currentPath, setCurrentPath } = useStore();
  const parts = currentPath.split('/').filter(Boolean);

  return (
    <div className="flex items-center space-x-1 text-sm text-muted-foreground mb-4 overflow-x-auto whitespace-nowrap pb-2">
      <button
        onClick={() => setCurrentPath('/')}
        className="hover:text-foreground transition-colors p-1 rounded-md hover:bg-accent flex-shrink-0"
      >
        <Home size={16} />
      </button>
      {parts.map((part, i) => (
        <React.Fragment key={i}>
          <ChevronRight size={14} className="flex-shrink-0" />
          <button
            onClick={() => setCurrentPath('/' + parts.slice(0, i + 1).join('/') + '/')}
            className="hover:text-foreground transition-colors px-2 py-1 rounded-md hover:bg-accent flex-shrink-0"
          >
            {part}
          </button>
        </React.Fragment>
      ))}
    </div>
  );
};

const FileTypeIcon = ({ type }: { type: string }) => {
  switch (type) {
    case 'image': return <Image size={18} className="text-pink-400" />;
    case 'video': return <Video size={18} className="text-purple-400" />;
    case 'audio': return <Music size={18} className="text-amber-400" />;
    case 'text': return <FileText size={18} className="text-blue-400" />;
    case 'archive': return <Archive size={18} className="text-orange-400" />;
    default: return <File size={18} className="text-slate-400" />;
  }
};

export const FileList: React.FC<{ currentFolder: FolderNode }> = ({ currentFolder }) => {
  const { setCurrentPath } = useStore();
  const children = currentFolder.children || [];

  if (children.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-muted-foreground opacity-50">
        <File size={48} className="mb-4" />
        <p>This folder is empty</p>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-0">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[50%]">Name</TableHead>
            <TableHead className="w-[15%]">Size</TableHead>
            <TableHead className="w-[20%]">Modified</TableHead>
            <TableHead className="w-[15%] text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
      </Table>
      <div className="flex-1 overflow-hidden">
        <Virtuoso
          style={{ height: '100%' }}
          data={children}
          itemContent={(_, node) => {
            const isFolder = 'isFolder' in node;
            return (
              <div
                className="flex items-center border-b hover:bg-muted/50 transition-colors cursor-pointer text-sm"
                onClick={() => isFolder ? setCurrentPath(node.path) : window.open(node.url, '_blank')}
              >
                <div className="w-[50%] p-4 flex items-center min-w-0">
                  {isFolder ? <File className="mr-3 text-sky-400 flex-shrink-0" /> : <FileTypeIcon type={node.type} />}
                  <span className="ml-3 truncate">{node.name}</span>
                </div>
                <div className="w-[15%] p-4 text-muted-foreground">
                  {isFolder ? '--' : formatSize(node.size)}
                </div>
                <div className="w-[20%] p-4 text-muted-foreground">
                  {isFolder ? '--' : new Date(node.modificationDate).toLocaleDateString()}
                </div>
                <div className="w-[15%] p-4 text-right">
                  {!isFolder && (
                    <a
                      href={node.url}
                      download
                      onClick={(e) => e.stopPropagation()}
                      className="p-2 opacity-0 group-hover:opacity-100 lg:opacity-100 hover:bg-accent rounded-md inline-block transition-all"
                    >
                      <Download size={16} />
                    </a>
                  )}
                </div>
              </div>
            );
          }}
        />
      </div>
    </div>
  );
};

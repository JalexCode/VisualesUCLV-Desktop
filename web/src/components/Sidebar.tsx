import React from 'react';
import { useStore } from '../store/useStore';
import { Folder, File, ChevronRight, ChevronDown, Star } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { FolderNode, RepoNode } from '../types';
import { cn } from '../lib/utils';

interface TreeItemProps {
  node: RepoNode;
  level: number;
}

const TreeItem: React.FC<TreeItemProps> = ({ node, level }) => {
  const { expandedFolders, toggleFolder, currentPath, setCurrentPath, toggleFavorite, favorites } = useStore();
  const isFolder = 'isFolder' in node;
  const isExpanded = expandedFolders.has(node.path);
  const isActive = currentPath === node.path;
  const isFavorite = favorites.has(node.path);

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isFolder) toggleFolder(node.path);
  };

  const handleClick = () => {
    if (isFolder) {
      setCurrentPath(node.path);
    }
  };

  return (
    <div className="select-none">
      <div
        className={cn(
          "group flex items-center py-1 px-2 cursor-pointer rounded-md transition-colors duration-200",
          isActive ? "bg-accent text-accent-foreground" : "hover:bg-accent/50 text-muted-foreground hover:text-foreground"
        )}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        onClick={handleClick}
      >
        <span onClick={handleToggle} className="w-4 h-4 mr-1 flex items-center justify-center">
          {isFolder && (
            isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />
          )}
        </span>
        {isFolder ? <Folder size={16} className="mr-2 text-sky-400" /> : <File size={16} className="mr-2 text-slate-400" />}
        <span className="text-sm truncate flex-1">{node.name}</span>

        <button
          onClick={(e) => { e.stopPropagation(); toggleFavorite(node.path); }}
          className={cn(
            "opacity-0 group-hover:opacity-100 p-1 hover:text-yellow-500 transition-all",
            isFavorite && "opacity-100 text-yellow-500"
          )}
        >
          <Star size={12} fill={isFavorite ? "currentColor" : "none"} />
        </button>
      </div>

      <AnimatePresence>
        {isFolder && isExpanded && node.children && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            {node.children.map((child) => (
              <TreeItem key={child.path} node={child} level={level + 1} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export const Sidebar: React.FC<{ data: FolderNode }> = ({ data }) => {
  return (
    <div className="w-64 h-full border-r bg-card flex flex-col overflow-hidden">
      <div className="p-4 border-b">
        <h1 className="text-lg font-bold text-sky-500 tracking-tight">Visuales UCLV</h1>
        <p className="text-xs text-muted-foreground">Explorer Web</p>
      </div>
      <div className="flex-1 overflow-y-auto p-2">
        <TreeItem node={data} level={0} />
      </div>
    </div>
  );
};

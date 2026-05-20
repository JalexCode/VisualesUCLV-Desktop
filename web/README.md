# Visuales UCLV Explorer Web

A modern, high-performance web-based media explorer for the Visuales UCLV FTP repository.

## Features

- **Modern UI/UX**: Inspired by Raycast and Arc Browser.
- **Fast Fuzzy Search**: Typo-tolerant instant search using Fuse.js.
- **Efficient Browsing**: Recursive tree explorer and breadcrumb navigation.
- **Virtualized Lists**: Smooth performance with thousands of files using React Virtuoso.
- **Dark Mode**: Premium dark aesthetic by default.
- **Static Deployment**: Fully compatible with GitHub Pages (No backend required).

## Tech Stack

- **Framework**: React + TypeScript + Vite
- **Styling**: TailwindCSS + Framer Motion + shadcn/ui
- **State**: Zustand
- **Search**: Fuse.js
- **Virtualization**: React Virtuoso

## Getting Started

1. `cd web`
2. `npm install`
3. `npm run dev`

## Build & Deploy

To build the project for production:
```bash
npm run build
```
The output will be in the `dist` folder, ready to be deployed to any static hosting service like GitHub Pages.

## Architectural Decisions

- **Client-Side Search**: We index the entire repository structure on the client using Fuse.js to provide instant, typo-tolerant search results without network latency.
- **Virtualized Rendering**: Using `react-virtuoso` ensures that only the visible items are rendered, keeping the UI responsive even with thousands of files.
- **Flat Data Indexing**: We flatten the tree structure for search indexing while maintaining the recursive structure for the sidebar, balancing search speed and navigation depth.

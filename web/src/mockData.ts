import type { FolderNode } from './types';

export const mockData: FolderNode = {
  name: 'Visuales UCLV',
  path: '/',
  isFolder: true,
  children: [
    {
      name: 'Movies',
      path: '/Movies/',
      isFolder: true,
      children: [
        {
          name: 'Action',
          path: '/Movies/Action/',
          isFolder: true,
          children: [
            {
              name: 'The Matrix.mp4',
              type: 'video',
              size: 2450000000,
              modificationDate: '2023-10-15T14:30:00Z',
              url: 'http://visuales.uclv.cu/Peliculas/The%20Matrix.mp4',
              path: '/Movies/Action/The Matrix.mp4'
            },
            {
              name: 'John Wick.mkv',
              type: 'video',
              size: 4800000000,
              modificationDate: '2024-01-20T09:15:00Z',
              url: 'http://visuales.uclv.cu/Peliculas/John%20Wick.mkv',
              path: '/Movies/Action/John Wick.mkv'
            }
          ]
        },
        {
          name: 'Comedy',
          path: '/Movies/Comedy/',
          isFolder: true,
          children: []
        }
      ]
    },
    {
      name: 'Music',
      path: '/Music/',
      isFolder: true,
      children: [
        {
          name: 'Rock',
          path: '/Music/Rock/',
          isFolder: true,
          children: []
        },
        {
            name: 'Song.mp3',
            type: 'audio',
            size: 5000000,
            modificationDate: '2023-12-01T10:00:00Z',
            url: 'http://visuales.uclv.cu/Musica/Song.mp3',
            path: '/Music/Song.mp3'
        }
      ]
    },
    {
      name: 'Documents',
      path: '/Documents/',
      isFolder: true,
      children: [
        {
          name: 'Readme.txt',
          type: 'text',
          size: 1024,
          modificationDate: '2024-05-19T10:00:00Z',
          url: 'http://visuales.uclv.cu/Docs/Readme.txt',
          path: '/Documents/Readme.txt'
        }
      ]
    }
  ]
};

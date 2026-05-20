import { openDB, type IDBPDatabase } from 'idb';

const DB_NAME = 'VisualesUCLV_DB';
const STORE_NAME = 'tree_data';
const DB_VERSION = 1;

let dbPromise: Promise<IDBPDatabase> | null = null;

function getDB() {
  if (!dbPromise) {
    dbPromise = openDB(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME);
        }
      },
    });
  }
  return dbPromise;
}

export async function saveTree(treeData: any) {
  const db = await getDB();
  await db.put(STORE_NAME, treeData, 'current_tree');
}

export async function loadTree() {
  const db = await getDB();
  return await db.get(STORE_NAME, 'current_tree');
}

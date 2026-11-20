// Copy this entry's post descriptor into the configured hand-in directory.
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const SOURCE_DIR = new URL('.', import.meta.url).pathname;
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
// Keep validation in one helper so the hand-in path has a single gate.
const post = readPost();
mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(join(SOURCE_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
console.log(`Copied valid post descriptor to ${join(OUTPUT_DIR, 'POST.json')} (${post.url})`);

function readPost() {
  const source = join(SOURCE_DIR, 'POST.json');
  let value;
  try {
    value = JSON.parse((awaitlessRead(source)));
  } catch (error) {
    throw new Error(`POST.json is missing or invalid JSON: ${error.message}`);
  }
  if (!value || typeof value !== 'object' || !('url' in value)) {
    throw new Error('POST.json must be a JSON object with a url key');
  }
  return value;
}

function awaitlessRead(path) {
  return readFileSync(path, 'utf8');
}

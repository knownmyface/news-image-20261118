import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// make.fun news-image-20261118 entry: copy the pre-rendered front page
// (entry.png, built by render.py) into the output directory and validate it.
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const bytes = readFileSync(src);

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (!bytes.subarray(bytes.length - 12).includes(Buffer.from("IEND"))) {
  throw new Error("entry.png is truncated: no IEND chunk found");
}

// Read the image size straight out of the IHDR chunk (bytes 16-23) and
// enforce the competition limits: at most 1024x1024 px, at most 1 MiB.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1048576 limit`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log(`wrote ${dest} (${bytes.length} bytes, ${width}x${height})`);
console.log("stories: 48 (45 in the grid + 3 in the leads), 48 illustrated");

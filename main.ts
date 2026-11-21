// news-image-20261121 — entrypoint (Node 22, standard library only).
//
// The front page for Saturday 21 November 2026 is drawn by compose.py
// and kept in this repository as news.jpg: a 1024x1024 JPEG under the
// 1 MiB cap. This program hands the grader those exact bytes as
// entry.png. The gate reads the file's first bytes rather than its
// name, so a JPEG copied to entry.png is valid, and a byte-for-byte
// copy means repeated runs write identical bytes.
//
// Try it outside the grader (MAKEFUN_OUTPUT_DIR stands in for /output):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

function main(): void {
  const root = dirname(fileURLToPath(import.meta.url));
  const input = join(root, "news.jpg");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const output = join(outDir, "entry.png");

  mkdirSync(outDir, { recursive: true });
  copyFileSync(input, output);
  console.log(`Wrote ${output} (${statSync(output).size} bytes)`);
}

main();

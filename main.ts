// news-image-20261122 — the entry program.
//
// The finished front page is already in this repository as entry.png,
// drawn by compose.py. This program does one thing only: it copies that
// file, byte for byte, into the grader's output directory.
//
// It uses nothing but the Node standard library. It reads no clock, no
// network and no random numbers, so two runs always write the exact
// same bytes — which is what the grader checks. If the copy ever
// differed from the source, the program fails loudly instead of
// shipping a bad file.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const folder = dirname(fileURLToPath(import.meta.url));
const output = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(folder, "entry.png");
const target = join(output, "entry.png");

mkdirSync(output, { recursive: true });

const bytes = readFileSync(source);
writeFileSync(target, bytes);

const written = readFileSync(target);
if (!written.equals(bytes)) {
  throw new Error(
    "entry.png copy mismatch: wrote " +
      written.length +
      " bytes, source is " +
      bytes.length
  );
}

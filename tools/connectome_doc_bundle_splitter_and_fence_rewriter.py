#!/usr/bin/env python3
# DOCS: docs/tools/PATTERNS_Tools.md
"""
Split a bundled connectome doc file into individual docs and rewrite fence markers.

The bundle format is:
  ### relative/path/to/doc.md
  <doc contents...>

This script writes each section to its path and replaces all "$$$" with "```".
"""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import sys
import re


def _is_safe_relative_path(raw_path: str) -> bool:
    if not raw_path:
        return False
    posix_path = PurePosixPath(raw_path)
    if posix_path.is_absolute():
        return False
    if ".." in posix_path.parts:
        return False
    return True


def _split_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_path: str | None = None
    buffer: list[str] = []
    header_re = re.compile(r"^###\s+(\S+\.md)\s*$")

    for line in text.splitlines():
        match = header_re.match(line)
        if match:
            if current_path is not None:
                sections.append((current_path, "\n".join(buffer).lstrip("\n")))
            current_path = match.group(1)
            buffer = []
            continue
        buffer.append(line)

    if current_path is not None:
        sections.append((current_path, "\n".join(buffer).lstrip("\n")))

    return sections


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Split connectome doc bundle into files and rewrite $$$ fences."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/connectome/1.md",
        help="Path to bundled markdown file",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to write files under (default: repo root)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    text = input_path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    sections = _split_sections(text)
    if not sections:
        print("No sections found (expected lines starting with '### ').", file=sys.stderr)
        return 1

    root = Path(args.root)
    written = 0
    for raw_path, content in sections:
        if not _is_safe_relative_path(raw_path):
            print(f"Skipping unsafe path: {raw_path}", file=sys.stderr)
            continue

        target_path = root / Path(raw_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        rewritten = content.replace("$$$", "```")
        target_path.write_text(rewritten.rstrip() + "\n", encoding="utf-8")
        written += 1

    print(f"Wrote {written} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

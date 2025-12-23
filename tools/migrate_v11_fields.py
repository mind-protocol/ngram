#!/usr/bin/env python3
"""
Schema v1.1 Field Migration Script

Migrates old field names to v1.1:
- tick_spoken → tick_resolved
- tick_decayed → tick_resolved
- status='spoken' → status='completed' (in code contexts only)

Usage:
    python tools/migrate_v11_fields.py --dry-run   # Preview changes
    python tools/migrate_v11_fields.py             # Apply changes
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# Root directory
ROOT = Path("/home/mind-protocol/ngram")

# Directories to process
TARGET_DIRS = [
    "engine",
    "tools",
    "agents",
]

# File extensions to process
EXTENSIONS = {".py", ".md", ".yaml", ".yml"}

# Files/dirs to skip
SKIP_PATTERNS = [
    "__pycache__",
    ".git",
    "node_modules",
    ".next",
    "archive",  # Don't migrate archived files
    "migrate_v11",  # Don't migrate migration scripts
    "migrate_schema",
]

# Replacements for Python code files
PY_REPLACEMENTS = [
    # Field name replacements (word boundary)
    (r'\btick_spoken\b', 'tick_resolved'),
    (r'\btick_decayed\b', 'tick_resolved'),
    # Status in code (careful: only in assignment/comparison contexts)
    (r"status\s*=\s*['\"]spoken['\"]", "status = 'completed'"),
    (r"status\s*==\s*['\"]spoken['\"]", "status == 'completed'"),
    (r"m\.status\s*=\s*['\"]spoken['\"]", "m.status = 'completed'"),
]

# Replacements for docs (more conservative)
DOC_REPLACEMENTS = [
    # Field names
    (r'\btick_spoken\b', 'tick_resolved'),
    (r'\btick_decayed\b', 'tick_resolved'),
    # Status in code blocks (triple backtick contexts)
    (r"status\s*=\s*['\"]spoken['\"]", "status = 'completed'"),
    (r"status\s*==\s*['\"]spoken['\"]", "status == 'completed'"),
]


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    path_str = str(path)
    for pattern in SKIP_PATTERNS:
        if pattern in path_str:
            return True
    return False


def migrate_file(path: Path, dry_run: bool = True) -> Tuple[int, List[str]]:
    """Migrate a single file. Returns (change_count, changes)."""
    if should_skip(path):
        return 0, []

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return 0, [f"Error reading: {e}"]

    original = content
    changes = []

    # Choose replacements based on file type
    if path.suffix == '.py':
        replacements = PY_REPLACEMENTS
    else:
        replacements = DOC_REPLACEMENTS

    for pattern, replacement in replacements:
        matches = re.findall(pattern, content)
        if matches:
            if not dry_run:
                content = re.sub(pattern, replacement, content)
            changes.append(f"  {pattern} → {replacement} ({len(matches)}x)")

    if content != original and not dry_run:
        path.write_text(content, encoding='utf-8')

    return len(changes), changes


def find_files() -> List[Path]:
    """Find all files to process."""
    files = []
    for dir_name in TARGET_DIRS:
        target_dir = ROOT / dir_name
        if not target_dir.exists():
            continue
        for ext in EXTENSIONS:
            files.extend(target_dir.rglob(f"*{ext}"))
    return [f for f in files if not should_skip(f)]


def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if dry_run:
        print("=" * 60)
        print("DRY RUN - No changes will be made")
        print("=" * 60)
    else:
        print("=" * 60)
        print("APPLYING CHANGES")
        print("=" * 60)

    files = find_files()
    print(f"\nScanning {len(files)} files...\n")

    total_files = 0
    total_changes = 0

    for path in sorted(files):
        count, changes = migrate_file(path, dry_run)
        if count > 0:
            rel = path.relative_to(ROOT)
            print(f"{rel}:")
            for c in changes:
                print(c)
            print()
            total_files += 1
            total_changes += count

    print("=" * 60)
    if dry_run:
        print(f"Would migrate {total_files} files with {total_changes} replacement patterns")
        print("\nRun without --dry-run to apply changes")
    else:
        print(f"Migrated {total_files} files with {total_changes} replacement patterns")


if __name__ == "__main__":
    main()

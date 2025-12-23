#!/usr/bin/env python3
"""
Schema v1.1 Migration Script

Renames:
- tick_spoken → tick_resolved
- tick_decayed → tick_resolved
- status = 'spoken' → status = 'completed'
- status = 'decayed' → status = 'rejected'
"""

import re
import sys
from pathlib import Path

# Files to migrate
TARGET_DIRS = [
    "engine/moment_graph",
    "engine/physics/graph",
    "engine/infrastructure",
    "engine/tests",
]

# Replacements (order matters for some)
REPLACEMENTS = [
    # Field renames
    (r'\btick_spoken\b', 'tick_resolved'),
    (r'\btick_decayed\b', 'tick_resolved'),
    
    # Status string replacements (careful with quotes)
    (r"status\s*=\s*['\"]spoken['\"]", "status = 'completed'"),
    (r"status\s*=\s*['\"]decayed['\"]", "status = 'rejected'"),
    
    # In lists/arrays
    (r"'spoken'", "'completed'"),
    (r'"spoken"', '"completed"'),
    (r"'decayed'", "'rejected'"),
    (r'"decayed"', '"rejected"'),
]

def migrate_file(path: Path) -> tuple[int, list[str]]:
    """Migrate a single file. Returns (change_count, changes)."""
    try:
        content = path.read_text()
    except Exception as e:
        return 0, [f"Error reading: {e}"]
    
    original = content
    changes = []
    
    for pattern, replacement in REPLACEMENTS:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes.append(f"  {pattern} → {replacement} ({len(matches)}x)")
    
    if content != original:
        path.write_text(content)
        return len(changes), changes
    
    return 0, []

def main():
    root = Path("/home/mind-protocol/ngram")
    total_files = 0
    total_changes = 0
    
    for dir_name in TARGET_DIRS:
        target_dir = root / dir_name
        if not target_dir.exists():
            print(f"Skipping {dir_name} (not found)")
            continue
        
        for path in target_dir.rglob("*.py"):
            count, changes = migrate_file(path)
            if count > 0:
                rel = path.relative_to(root)
                print(f"\n{rel}:")
                for c in changes:
                    print(c)
                total_files += 1
                total_changes += count
    
    print(f"\n{'='*50}")
    print(f"Migrated {total_files} files with {total_changes} replacement patterns")

if __name__ == "__main__":
    main()

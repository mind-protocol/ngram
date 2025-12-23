#!/usr/bin/env python3
"""
Migration 001: Align DB labels with schema.yaml

Renames:
- Character → Actor
- Place → Space

No backwards compatibility. Run once, verify, done.

Usage:
    python -m engine.migrations.migrate_001_schema_alignment --graph seed
    python -m engine.migrations.migrate_001_schema_alignment --graph blood_ledger --dry-run
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from falkordb import FalkorDB
    FALKORDB_AVAILABLE = True
except ImportError:
    FALKORDB_AVAILABLE = False


def migrate(graph, dry_run: bool = False) -> dict:
    """
    Migrate graph labels from Character/Place to Actor/Space.

    Returns dict with migration stats.
    """
    stats = {
        'characters_before': 0,
        'places_before': 0,
        'actors_after': 0,
        'spaces_after': 0,
        'errors': []
    }

    # Count before
    try:
        result = graph.query("MATCH (n:Character) RETURN count(n)")
        stats['characters_before'] = result.result_set[0][0] if result.result_set else 0
    except Exception as e:
        stats['errors'].append(f"Count Character: {e}")

    try:
        result = graph.query("MATCH (n:Place) RETURN count(n)")
        stats['places_before'] = result.result_set[0][0] if result.result_set else 0
    except Exception as e:
        stats['errors'].append(f"Count Place: {e}")

    print(f"Before migration:")
    print(f"  Character nodes: {stats['characters_before']}")
    print(f"  Place nodes: {stats['places_before']}")

    if dry_run:
        print("\n[DRY RUN] Would migrate:")
        print(f"  {stats['characters_before']} Character → Actor")
        print(f"  {stats['places_before']} Place → Space")
        return stats

    # Migrate Character → Actor
    if stats['characters_before'] > 0:
        print("\nMigrating Character → Actor...")
        try:
            graph.query("MATCH (n:Character) SET n:Actor REMOVE n:Character")
            print("  Done.")
        except Exception as e:
            stats['errors'].append(f"Migrate Character→Actor: {e}")
            print(f"  ERROR: {e}")

    # Migrate Place → Space
    if stats['places_before'] > 0:
        print("Migrating Place → Space...")
        try:
            graph.query("MATCH (n:Place) SET n:Space REMOVE n:Place")
            print("  Done.")
        except Exception as e:
            stats['errors'].append(f"Migrate Place→Space: {e}")
            print(f"  ERROR: {e}")

    # Verify
    print("\nVerifying...")

    try:
        result = graph.query("MATCH (n:Character) RETURN count(n)")
        remaining_chars = result.result_set[0][0] if result.result_set else 0
        if remaining_chars > 0:
            stats['errors'].append(f"{remaining_chars} Character nodes still exist")
            print(f"  WARNING: {remaining_chars} Character nodes remain!")
    except Exception as e:
        stats['errors'].append(f"Verify Character: {e}")

    try:
        result = graph.query("MATCH (n:Place) RETURN count(n)")
        remaining_places = result.result_set[0][0] if result.result_set else 0
        if remaining_places > 0:
            stats['errors'].append(f"{remaining_places} Place nodes still exist")
            print(f"  WARNING: {remaining_places} Place nodes remain!")
    except Exception as e:
        stats['errors'].append(f"Verify Place: {e}")

    try:
        result = graph.query("MATCH (n:Actor) RETURN count(n)")
        stats['actors_after'] = result.result_set[0][0] if result.result_set else 0
    except Exception as e:
        stats['errors'].append(f"Count Actor: {e}")

    try:
        result = graph.query("MATCH (n:Space) RETURN count(n)")
        stats['spaces_after'] = result.result_set[0][0] if result.result_set else 0
    except Exception as e:
        stats['errors'].append(f"Count Space: {e}")

    print(f"\nAfter migration:")
    print(f"  Actor nodes: {stats['actors_after']}")
    print(f"  Space nodes: {stats['spaces_after']}")

    if stats['errors']:
        print(f"\nErrors: {len(stats['errors'])}")
        for err in stats['errors']:
            print(f"  - {err}")
    else:
        print("\nMigration successful!")

    return stats


def main():
    parser = argparse.ArgumentParser(description='Migrate graph labels to schema.yaml alignment')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--graph', required=True, help='Graph name to migrate')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without doing it')
    args = parser.parse_args()

    if not FALKORDB_AVAILABLE:
        print("ERROR: falkordb package not installed")
        print("  pip install falkordb")
        return 1

    try:
        db = FalkorDB(host=args.host, port=args.port)
        graph = db.select_graph(args.graph)
        print(f"Connected to FalkorDB: {args.graph} at {args.host}:{args.port}")
    except Exception as e:
        print(f"ERROR: Cannot connect to FalkorDB: {e}")
        print("  Start FalkorDB with: docker run -p 6379:6379 falkordb/falkordb")
        return 1

    stats = migrate(graph, dry_run=args.dry_run)

    return 0 if not stats['errors'] else 1


if __name__ == "__main__":
    sys.exit(main())

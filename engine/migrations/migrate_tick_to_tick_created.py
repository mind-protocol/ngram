#!/usr/bin/env python3
"""
Migration: Rename Moment.tick to Moment.tick_created

This migration renames the `tick` property on all Moment nodes to `tick_created`
to align with the updated Pydantic model schema.

Run: python3 -m engine.migrations.migrate_tick_to_tick_created

Decision: 2025-12-23 - No backwards compat. All graphs migrated immediately.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def migrate(graph_name: str = "blood_ledger", host: str = "localhost", port: int = 6379):
    """
    Migrate all Moment nodes: rename tick -> tick_created.

    Args:
        graph_name: Name of the FalkorDB graph
        host: Redis host
        port: Redis port
    """
    from falkordb import FalkorDB

    print(f"Connecting to {host}:{port}, graph: {graph_name}")
    db = FalkorDB(host=host, port=port)
    graph = db.select_graph(graph_name)

    # Check how many moments have the old 'tick' property
    result = graph.query("MATCH (m:Moment) WHERE m.tick IS NOT NULL RETURN count(m) as count")
    count = result.result_set[0][0] if result.result_set else 0
    print(f"Found {count} Moment nodes with 'tick' property")

    if count == 0:
        print("Nothing to migrate.")
        return

    # Migrate: copy tick to tick_created, then remove tick
    print("Migrating tick -> tick_created...")
    graph.query("""
        MATCH (m:Moment)
        WHERE m.tick IS NOT NULL AND m.tick_created IS NULL
        SET m.tick_created = m.tick
        REMOVE m.tick
    """)

    # Verify
    result = graph.query("MATCH (m:Moment) WHERE m.tick IS NOT NULL RETURN count(m) as count")
    remaining = result.result_set[0][0] if result.result_set else 0

    if remaining == 0:
        print(f"✓ Successfully migrated {count} Moment nodes")
    else:
        print(f"⚠ Warning: {remaining} nodes still have 'tick' property")

    # Show sample of migrated data
    result = graph.query("MATCH (m:Moment) RETURN m.id, m.tick_created LIMIT 3")
    if result.result_set:
        print("\nSample migrated moments:")
        for row in result.result_set:
            print(f"  {row[0]}: tick_created={row[1]}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate Moment.tick to Moment.tick_created")
    parser.add_argument("--graph", default="blood_ledger", help="Graph name")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated without making changes")

    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN - no changes will be made")
        from falkordb import FalkorDB
        db = FalkorDB(host=args.host, port=args.port)
        graph = db.select_graph(args.graph)
        result = graph.query("MATCH (m:Moment) WHERE m.tick IS NOT NULL RETURN count(m) as count")
        count = result.result_set[0][0] if result.result_set else 0
        print(f"Would migrate {count} Moment nodes")
    else:
        migrate(args.graph, args.host, args.port)

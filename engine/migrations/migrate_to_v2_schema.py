"""
Migration: Align graphs to Schema v2

Performs:
1. Label renames: Character → Actor, Place → Space
2. Add default physics fields: energy, weight on all nodes
3. Add default link fields: energy, weight, conductivity, strength

Usage:
    python -m engine.migrations.migrate_to_v2_schema all
    python -m engine.migrations.migrate_to_v2_schema blood_ledger seed test
    python -m engine.migrations.migrate_to_v2_schema --dry-run blood_ledger

DOCS: docs/schema/MIGRATION_Schema_Alignment.md
"""

import argparse
import logging
import sys
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class MigrationResult:
    """Result of a single graph migration."""
    graph_name: str
    success: bool
    labels_renamed: Dict[str, int]
    fields_renamed: Dict[str, int]
    nodes_updated: int
    links_updated: int
    errors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_name": self.graph_name,
            "success": self.success,
            "labels_renamed": self.labels_renamed,
            "fields_renamed": self.fields_renamed,
            "nodes_updated": self.nodes_updated,
            "links_updated": self.links_updated,
            "errors": self.errors,
        }


# Default physics values per schema.yaml
DEFAULTS = {
    "node": {
        "energy": 0.0,
        "weight": 0.5,
    },
    "link": {
        "energy": 0.0,
        "weight": 1.0,
        "conductivity": 1.0,
        "strength": 0.0,
    },
}

# Deprecated field renames (old → new)
FIELD_RENAMES = {
    "detail": "description",  # Actor.detail → description (per schema.yaml)
}


def get_graph_connection(graph_name: str, host: str = "localhost", port: int = 6379):
    """Get FalkorDB graph connection."""
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host=host, port=port)
        return db.select_graph(graph_name)
    except ImportError:
        # Fallback to redis direct
        import redis
        r = redis.Redis(host=host, port=port, decode_responses=True)
        return RedisGraphWrapper(r, graph_name)


class RedisGraphWrapper:
    """Minimal wrapper for redis GRAPH commands."""

    def __init__(self, redis_client, graph_name: str):
        self.redis = redis_client
        self.graph_name = graph_name

    def query(self, cypher: str):
        """Execute Cypher query."""
        result = self.redis.execute_command("GRAPH.QUERY", self.graph_name, cypher)
        return self._parse_result(result)

    def _parse_result(self, result):
        """Parse redis GRAPH.QUERY result."""
        if not result or len(result) < 2:
            return []
        # First element is header, second is data rows
        headers = result[0] if result[0] else []
        rows = result[1] if len(result) > 1 else []

        # Return as list of dicts
        parsed = []
        for row in rows:
            if headers:
                parsed.append(dict(zip(headers, row)))
            else:
                parsed.append(row)
        return parsed


def migrate_graph(
    graph_name: str,
    host: str = "localhost",
    port: int = 6379,
    dry_run: bool = False
) -> MigrationResult:
    """
    Migrate a single graph to v2 schema.

    Steps:
    1. Rename Character → Actor (if exists)
    2. Rename Place → Space (if exists)
    3. Rename deprecated fields (detail → description)
    4. Add energy/weight defaults to all nodes missing them
    5. Add energy/weight/conductivity/strength to all links missing them
    """
    errors = []
    labels_renamed = {}
    fields_renamed = {}
    nodes_updated = 0
    links_updated = 0

    try:
        graph = get_graph_connection(graph_name, host, port)

        # Step 1: Check for old labels
        old_labels = _check_old_labels(graph)
        logger.info(f"[{graph_name}] Old labels found: {old_labels}")

        if not dry_run:
            # Step 2: Rename Character → Actor
            if old_labels.get("Character", 0) > 0:
                count = _rename_label(graph, "Character", "Actor")
                labels_renamed["Character→Actor"] = count
                logger.info(f"[{graph_name}] Renamed {count} Character → Actor")

            # Step 3: Rename Place → Space
            if old_labels.get("Place", 0) > 0:
                count = _rename_label(graph, "Place", "Space")
                labels_renamed["Place→Space"] = count
                logger.info(f"[{graph_name}] Renamed {count} Place → Space")

            # Step 4: Rename deprecated fields
            fields_renamed = _rename_deprecated_fields(graph)
            if fields_renamed:
                logger.info(f"[{graph_name}] Fields renamed: {fields_renamed}")

            # Step 5: Add node defaults
            nodes_updated = _add_node_defaults(graph)
            logger.info(f"[{graph_name}] Updated {nodes_updated} nodes with defaults")

            # Step 6: Add link defaults
            links_updated = _add_link_defaults(graph)
            logger.info(f"[{graph_name}] Updated {links_updated} links with defaults")
        else:
            logger.info(f"[{graph_name}] DRY RUN - no changes made")

        return MigrationResult(
            graph_name=graph_name,
            success=True,
            labels_renamed=labels_renamed,
            fields_renamed=fields_renamed,
            nodes_updated=nodes_updated,
            links_updated=links_updated,
            errors=errors,
        )

    except Exception as e:
        logger.exception(f"[{graph_name}] Migration failed")
        errors.append(str(e))
        return MigrationResult(
            graph_name=graph_name,
            success=False,
            labels_renamed=labels_renamed,
            fields_renamed=fields_renamed,
            nodes_updated=nodes_updated,
            links_updated=links_updated,
            errors=errors,
        )


def _extract_count(result) -> int:
    """Extract count from FalkorDB QueryResult or redis result."""
    try:
        # FalkorDB QueryResult has .result_set
        if hasattr(result, 'result_set'):
            rs = result.result_set
            if rs and len(rs) > 0:
                row = rs[0]
                return int(row[0]) if row else 0
        # Redis wrapper returns list of dicts
        elif isinstance(result, list) and len(result) > 0:
            row = result[0]
            if isinstance(row, dict):
                return int(row.get('cnt', 0) or 0)
            return int(row[0]) if row else 0
        return 0
    except:
        return 0


def _check_old_labels(graph) -> Dict[str, int]:
    """Check for old v1 labels."""
    counts = {}
    for label in ["Character", "Place"]:
        try:
            result = graph.query(f"MATCH (n:{label}) RETURN count(n) AS cnt")
            counts[label] = _extract_count(result)
        except:
            counts[label] = 0
    return counts


def _rename_label(graph, old_label: str, new_label: str) -> int:
    """Rename all nodes with old_label to new_label."""
    # FalkorDB uses: SET n:NewLabel REMOVE n:OldLabel
    query = f"""
    MATCH (n:{old_label})
    SET n:{new_label}
    REMOVE n:{old_label}
    RETURN count(n) AS cnt
    """
    try:
        result = graph.query(query)
        return _extract_count(result)
    except Exception as e:
        logger.warning(f"Label rename failed: {e}")
    return 0


def _add_node_defaults(graph) -> int:
    """Add default energy/weight to nodes missing them."""
    total = 0

    # Update nodes missing energy
    try:
        result = graph.query(f"""
        MATCH (n)
        WHERE n.energy IS NULL
        SET n.energy = {DEFAULTS['node']['energy']}
        RETURN count(n) AS cnt
        """)
        total += _extract_count(result)
    except Exception as e:
        logger.warning(f"Failed to set node energy defaults: {e}")

    # Update nodes missing weight
    try:
        result = graph.query(f"""
        MATCH (n)
        WHERE n.weight IS NULL
        SET n.weight = {DEFAULTS['node']['weight']}
        RETURN count(n) AS cnt
        """)
        total += _extract_count(result)
    except Exception as e:
        logger.warning(f"Failed to set node weight defaults: {e}")

    return total


def _add_link_defaults(graph) -> int:
    """Add default physics fields to links missing them."""
    total = 0

    for field, default in DEFAULTS['link'].items():
        try:
            result = graph.query(f"""
            MATCH ()-[r]->()
            WHERE r.{field} IS NULL
            SET r.{field} = {default}
            RETURN count(r) AS cnt
            """)
            total += _extract_count(result)
        except Exception as e:
            logger.warning(f"Failed to set link {field} defaults: {e}")

    return total


def _rename_deprecated_fields(graph) -> Dict[str, int]:
    """Rename deprecated fields to their new names."""
    renamed = {}

    for old_field, new_field in FIELD_RENAMES.items():
        try:
            # Copy old field value to new field, then remove old field
            result = graph.query(f"""
            MATCH (n)
            WHERE n.{old_field} IS NOT NULL AND n.{new_field} IS NULL
            SET n.{new_field} = n.{old_field}
            REMOVE n.{old_field}
            RETURN count(n) AS cnt
            """)
            count = _extract_count(result)
            if count > 0:
                renamed[f"{old_field}→{new_field}"] = count
        except Exception as e:
            logger.warning(f"Failed to rename field {old_field} → {new_field}: {e}")

    return renamed


def load_physics_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load physics configuration from YAML.

    Args:
        config_path: Path to config file. If None, uses default location.

    Returns:
        Config dict with defaults, by_label, by_type, by_id sections.
    """
    import yaml as yaml_module
    from pathlib import Path

    if config_path is None:
        # Default location
        config_path = Path(__file__).parent.parent / "data" / "physics_config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        logger.warning(f"Physics config not found: {config_path}")
        return {}

    try:
        with open(config_path) as f:
            config = yaml_module.safe_load(f)
        return config or {}
    except Exception as e:
        logger.warning(f"Failed to load physics config: {e}")
        return {}


def apply_physics_config(
    graph,
    config: Dict[str, Any],
    overwrite: bool = True
) -> Dict[str, int]:
    """
    Apply physics configuration to graph nodes and links.

    Args:
        graph: FalkorDB graph connection
        config: Physics config dict from load_physics_config()
        overwrite: If True, overwrite existing values. If False, only set missing.

    Returns:
        Dict with counts of updated nodes/links per category.
    """
    results = {"nodes": 0, "links": 0}

    if not config:
        return results

    defaults = config.get("defaults", {})
    by_label = config.get("by_label", {})
    by_type = config.get("by_type", {})
    by_id = config.get("by_id", {})
    link_by_type = config.get("link_by_type", {})

    # 1. Apply per-label defaults
    for label, values in by_label.items():
        if not values:
            continue
        for field, value in values.items():
            if value is None:
                continue
            try:
                if overwrite:
                    result = graph.query(f"""
                    MATCH (n:{label})
                    SET n.{field} = {value}
                    RETURN count(n) AS cnt
                    """)
                else:
                    result = graph.query(f"""
                    MATCH (n:{label})
                    WHERE n.{field} IS NULL
                    SET n.{field} = {value}
                    RETURN count(n) AS cnt
                    """)
                results["nodes"] += _extract_count(result)
            except Exception as e:
                logger.warning(f"Failed to apply {label}.{field}={value}: {e}")

    # 2. Apply per-type within label
    for label, type_configs in by_type.items():
        if not type_configs:
            continue
        for type_value, values in type_configs.items():
            if not values:
                continue
            for field, value in values.items():
                if value is None:
                    continue
                try:
                    if overwrite:
                        result = graph.query(f"""
                        MATCH (n:{label} {{type: '{type_value}'}})
                        SET n.{field} = {value}
                        RETURN count(n) AS cnt
                        """)
                    else:
                        result = graph.query(f"""
                        MATCH (n:{label} {{type: '{type_value}'}})
                        WHERE n.{field} IS NULL
                        SET n.{field} = {value}
                        RETURN count(n) AS cnt
                        """)
                    results["nodes"] += _extract_count(result)
                except Exception as e:
                    logger.warning(f"Failed to apply {label}.{type_value}.{field}={value}: {e}")

    # 3. Apply per-id overrides
    if by_id and by_id != {"pass": None}:
        for node_id, values in by_id.items():
            if not values or node_id == "pass":
                continue
            for field, value in values.items():
                if value is None:
                    continue
                try:
                    # Handle emotions specially (it's a list)
                    if field == "emotions":
                        value_str = str(value).replace("'", '"')
                        result = graph.query(f"""
                        MATCH (n {{id: '{node_id}'}})
                        SET n.emotions = '{value_str}'
                        RETURN count(n) AS cnt
                        """)
                    else:
                        result = graph.query(f"""
                        MATCH (n {{id: '{node_id}'}})
                        SET n.{field} = {value}
                        RETURN count(n) AS cnt
                        """)
                    results["nodes"] += _extract_count(result)
                except Exception as e:
                    logger.warning(f"Failed to apply {node_id}.{field}={value}: {e}")

    # 4. Apply link physics by relationship type
    for rel_type, values in link_by_type.items():
        if not values:
            continue
        for field, value in values.items():
            if value is None:
                continue
            try:
                if overwrite:
                    result = graph.query(f"""
                    MATCH ()-[r:{rel_type}]->()
                    SET r.{field} = {value}
                    RETURN count(r) AS cnt
                    """)
                else:
                    result = graph.query(f"""
                    MATCH ()-[r:{rel_type}]->()
                    WHERE r.{field} IS NULL
                    SET r.{field} = {value}
                    RETURN count(r) AS cnt
                    """)
                results["links"] += _extract_count(result)
            except Exception as e:
                logger.warning(f"Failed to apply link {rel_type}.{field}={value}: {e}")

    return results


def list_graphs(host: str = "localhost", port: int = 6379) -> List[str]:
    """List all graphs in the database."""
    import redis
    r = redis.Redis(host=host, port=port, decode_responses=True)
    result = r.execute_command("GRAPH.LIST")
    return list(result) if result else []


def migrate_all(
    host: str = "localhost",
    port: int = 6379,
    dry_run: bool = False,
    exclude: Optional[List[str]] = None
) -> List[MigrationResult]:
    """Migrate all graphs."""
    exclude = exclude or []
    graphs = list_graphs(host, port)
    results = []

    for graph_name in graphs:
        if graph_name in exclude:
            logger.info(f"Skipping excluded graph: {graph_name}")
            continue

        logger.info(f"Migrating: {graph_name}")
        result = migrate_graph(graph_name, host, port, dry_run)
        results.append(result)

    return results


def print_result(result: MigrationResult):
    """Print migration result."""
    status = "\033[92m✓\033[0m" if result.success else "\033[91m✗\033[0m"
    print(f"{status} {result.graph_name}")

    if result.labels_renamed:
        for rename, count in result.labels_renamed.items():
            print(f"    Labels: {rename} ({count})")

    if result.fields_renamed:
        for rename, count in result.fields_renamed.items():
            print(f"    Fields: {rename} ({count})")

    if result.nodes_updated:
        print(f"    Nodes: {result.nodes_updated} updated with defaults")

    if result.links_updated:
        print(f"    Links: {result.links_updated} updated with defaults")

    if result.errors:
        for error in result.errors:
            print(f"    \033[91mError: {error}\033[0m")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate FalkorDB graphs to Schema v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "graphs",
        nargs="*",
        default=["all"],
        help="Graph names to migrate (or 'all')"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--exclude", nargs="*", default=[], help="Graphs to exclude")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--apply-physics", action="store_true",
                        help="Apply physics config (energy/weight/conductivity)")
    parser.add_argument("--physics-config", default=None,
                        help="Path to physics_config.yaml (default: engine/data/physics_config.yaml)")
    parser.add_argument("--no-overwrite", action="store_true",
                        help="Only set physics values if currently NULL")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    if args.dry_run:
        print("\n\033[93m=== DRY RUN MODE ===\033[0m\n")

    # Run migrations
    if "all" in args.graphs:
        results = migrate_all(args.host, args.port, args.dry_run, args.exclude)
    else:
        results = []
        for graph_name in args.graphs:
            result = migrate_graph(graph_name, args.host, args.port, args.dry_run)
            results.append(result)

    # Print results
    print("\n\033[1mMigration Results:\033[0m\n")
    for result in results:
        print_result(result)

    # Summary
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count
    print(f"\n{success_count} succeeded, {fail_count} failed\n")

    # Apply physics config if requested
    if args.apply_physics and not args.dry_run:
        print("\n\033[1mApplying Physics Config:\033[0m\n")
        config = load_physics_config(args.physics_config)
        if config:
            overwrite = not args.no_overwrite
            for graph_name in args.graphs if "all" not in args.graphs else [r.graph_name for r in results]:
                if graph_name in args.exclude:
                    continue
                try:
                    graph = get_graph_connection(graph_name, args.host, args.port)
                    physics_result = apply_physics_config(graph, config, overwrite=overwrite)
                    mode = "overwrite" if overwrite else "fill-missing"
                    print(f"  \033[92m✓\033[0m {graph_name}: {physics_result['nodes']} node updates, "
                          f"{physics_result['links']} link updates ({mode})")
                except Exception as e:
                    print(f"  \033[91m✗\033[0m {graph_name}: {e}")
        else:
            print("  \033[93m!\033[0m No physics config found")

    # Exit code
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()

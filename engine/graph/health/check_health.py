#!/usr/bin/env python3
"""
Graph Health Check (v1.2)

Validates all nodes and links in the graph against the schema definition.
Reports missing required attributes, invalid enum values, and other issues.

v1.2 CHANGES:
  - 9 link types: 4 energy carriers (expresses, about, relates, attached_to)
                  5 structural (contains, leads_to, sequence, primes, can_become)
  - 5 node types: Actor, Space, Thing, Narrative, Moment
  - Physics validation: energy >= 0, conductivity in [0,1], weight >= 0
  - Link endpoint validation: node_a/node_b must exist
  - Deprecated link tracking: BELIEVES, AT, CARRIES, LOCATED_AT, CONNECTS

DOCS: docs/schema/graph-health/PATTERNS_Graph_Health_Validation.md

Usage:
    python engine/graph/health/check_health.py
    python engine/graph/health/check_health.py --graph seed
    python engine/graph/health/check_health.py --verbose
    python engine/graph/health/check_health.py --fix  # Future: auto-fix issues
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engine.physics.graph.graph_ops import GraphOps

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Schema paths
# Base schema (authoritative) - defines node_type, type as free string
BASE_SCHEMA_PATH = PROJECT_ROOT / "docs" / "schema" / "schema.yaml"
# Project-specific schema - adds Graph Engine enums for type values
PROJECT_SCHEMA_PATH = Path(__file__).parent / "schema.yaml"

# =============================================================================
# v1.2 LINK TYPES
# =============================================================================

# Energy carrier links (4)
ENERGY_CARRIER_LINKS = ["EXPRESSES", "ABOUT", "RELATES", "ATTACHED_TO"]

# Structural links (5)
STRUCTURAL_LINKS = ["CONTAINS", "LEADS_TO", "SEQUENCE", "PRIMES", "CAN_BECOME"]

# All v1.2 link types
V1_2_LINK_TYPES = ENERGY_CARRIER_LINKS + STRUCTURAL_LINKS

# Deprecated link types (v1.1 → v1.2 migration)
DEPRECATED_LINK_TYPES = ["BELIEVES", "AT", "CARRIES", "LOCATED_AT", "CONNECTS"]

# All link types to check (v1.2 + deprecated for migration tracking)
ALL_LINK_TYPES = V1_2_LINK_TYPES + DEPRECATED_LINK_TYPES

# =============================================================================
# v1.2 NODE TYPES
# =============================================================================

NODE_TYPES = ["Actor", "Space", "Thing", "Narrative", "Moment"]


@dataclass
class Issue:
    """A single validation issue."""
    node_type: str
    node_id: str
    issue_type: str  # missing_required, invalid_enum, missing_optional, type_error
    field: str
    message: str
    severity: str = "error"  # error, warning, info


@dataclass
class HealthReport:
    """Complete health report for the graph."""
    graph_name: str
    total_nodes: Dict[str, int] = field(default_factory=dict)
    total_links: Dict[str, int] = field(default_factory=dict)
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == "error"])

    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == "warning"])

    @property
    def is_healthy(self) -> bool:
        return self.error_count == 0

    def to_dict(self) -> Dict:
        return {
            "graph_name": self.graph_name,
            "healthy": self.is_healthy,
            "total_nodes": self.total_nodes,
            "total_links": self.total_links,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [
                {
                    "node_type": i.node_type,
                    "node_id": i.node_id,
                    "issue_type": i.issue_type,
                    "field": i.field,
                    "message": i.message,
                    "severity": i.severity,
                }
                for i in self.issues
            ]
        }

    def print_summary(self, verbose: bool = False):
        """Print a human-readable summary."""
        print(f"\n{'='*60}")
        print(f"Graph Health Report: {self.graph_name}")
        print(f"{'='*60}")

        print(f"\n--- Node Counts ---")
        for node_type, count in sorted(self.total_nodes.items()):
            print(f"  {node_type}: {count}")

        print(f"\n--- Link Counts ---")
        for link_type, count in sorted(self.total_links.items()):
            print(f"  {link_type}: {count}")

        print(f"\n--- Health Status ---")
        if self.is_healthy:
            print(f"  ✓ HEALTHY (no errors)")
        else:
            print(f"  ✗ UNHEALTHY ({self.error_count} errors, {self.warning_count} warnings)")

        if self.issues:
            # Group issues by type
            by_type: Dict[str, List[Issue]] = {}
            for issue in self.issues:
                key = f"{issue.node_type}:{issue.issue_type}"
                if key not in by_type:
                    by_type[key] = []
                by_type[key].append(issue)

            print(f"\n--- Issues by Category ---")
            for key, issues in sorted(by_type.items()):
                print(f"\n  [{key}] ({len(issues)} issues)")
                if verbose:
                    for issue in issues[:10]:  # Show first 10
                        severity_icon = "✗" if issue.severity == "error" else "⚠"
                        print(f"    {severity_icon} {issue.node_id}.{issue.field}: {issue.message}")
                    if len(issues) > 10:
                        print(f"    ... and {len(issues) - 10} more")
                else:
                    # Just show a sample
                    sample = issues[0]
                    print(f"    Example: {sample.node_id}.{sample.field}: {sample.message}")

        print(f"\n{'='*60}\n")


def load_schema() -> Dict:
    """Load the schema definition.

    Loads base schema from docs/schema/schema.yaml (authoritative),
    then overlays project-specific schema for Graph Engine enums.
    """
    schema = {}

    # Load base schema (authoritative)
    if BASE_SCHEMA_PATH.exists():
        with open(BASE_SCHEMA_PATH, 'r') as f:
            base = yaml.safe_load(f)
            # Convert base schema format to validation format
            schema['nodes'] = {}
            schema['links'] = {}

            # Extract node types from base schema
            if 'nodes' in base:
                for node_type, node_def in base['nodes'].items():
                    schema['nodes'][node_type.capitalize()] = {
                        'required': ['id', 'name'],
                        'optional': [],
                        'enums': {}
                    }

            # Extract invariants
            if 'invariants' in base:
                schema['invariants'] = base['invariants']

            logger.info(f"Loaded base schema from {BASE_SCHEMA_PATH}")

    # Overlay project-specific schema (Graph Engine enums)
    if PROJECT_SCHEMA_PATH.exists():
        with open(PROJECT_SCHEMA_PATH, 'r') as f:
            project = yaml.safe_load(f)
            # Merge project schema (overrides base)
            if 'nodes' in project:
                for node_type, node_def in project['nodes'].items():
                    if node_type not in schema.get('nodes', {}):
                        schema['nodes'][node_type] = {}
                    schema['nodes'][node_type].update(node_def)
            if 'links' in project:
                schema['links'] = project.get('links', {})
            logger.info(f"Loaded project schema from {PROJECT_SCHEMA_PATH}")

    if not schema:
        logger.warning("No schema found!")

    return schema


def validate_node(node: Dict, node_type: str, schema: Dict, report: HealthReport):
    """Validate a single node against the schema."""
    node_schema = schema['nodes'].get(node_type)
    if not node_schema:
        report.add_issue(Issue(
            node_type=node_type,
            node_id=node.get('id', 'unknown'),
            issue_type="unknown_type",
            field="",
            message=f"Unknown node type: {node_type}",
            severity="error"
        ))
        return

    node_id = node.get('id', 'unknown')

    # Check required fields
    for field in node_schema.get('required', []):
        if field not in node or node[field] is None or node[field] == '':
            report.add_issue(Issue(
                node_type=node_type,
                node_id=node_id,
                issue_type="missing_required",
                field=field,
                message=f"Missing required field: {field}",
                severity="error"
            ))

    # Check enum values
    enums = node_schema.get('enums', {})
    for field, valid_values in enums.items():
        if field in node and node[field] is not None:
            value = node[field]
            if value not in valid_values and value != '':
                report.add_issue(Issue(
                    node_type=node_type,
                    node_id=node_id,
                    issue_type="invalid_enum",
                    field=field,
                    message=f"Invalid value '{value}' for {field}. Valid: {valid_values}",
                    severity="warning"
                ))


def validate_link(link: Dict, link_type: str, schema: Dict, report: HealthReport):
    """Validate a single link against the schema."""
    link_schema = schema['links'].get(link_type)
    if not link_schema:
        # Unknown link type - might be okay
        return

    # For links, we mainly check enum values if present
    enums = link_schema.get('enums', {})
    link_id = f"{link.get('from', '?')}->{link.get('to', '?')}"

    for field, valid_values in enums.items():
        if field in link and link[field] is not None:
            value = link[field]
            if value not in valid_values:
                report.add_issue(Issue(
                    node_type=link_type,
                    node_id=link_id,
                    issue_type="invalid_enum",
                    field=field,
                    message=f"Invalid value '{value}' for {field}. Valid: {valid_values}",
                    severity="warning"
                ))


def check_graph_health(graph: GraphOps, schema: Dict) -> HealthReport:
    """Run health checks on the entire graph.

    v1.2: Validates all 6 node types and 9 link types (+ deprecated).
    """
    report = HealthReport(graph_name=graph.graph_name)

    # =========================================================================
    # NODE VALIDATION (6 types)
    # =========================================================================

    for node_type in NODE_TYPES:
        logger.info(f"Checking {node_type}s...")
        try:
            result = graph._query(f"MATCH (n:{node_type}) RETURN n")
            nodes = [dict(row[0].properties) for row in result] if result else []
            report.total_nodes[node_type] = len(nodes)
            for node in nodes:
                validate_node(node, node_type, schema, report)
        except Exception as e:
            logger.warning(f"Error querying {node_type}: {e}")
            report.total_nodes[node_type] = 0

    # =========================================================================
    # LINK COUNTING (v1.2 + deprecated)
    # =========================================================================

    logger.info("Checking Links...")

    # Count v1.2 link types
    for link_type in V1_2_LINK_TYPES:
        try:
            result = graph._query(f"MATCH ()-[r:{link_type}]->() RETURN count(r)")
            report.total_links[link_type] = result[0][0] if result else 0
        except Exception as e:
            logger.warning(f"Error counting {link_type}: {e}")
            report.total_links[link_type] = 0

    # Count deprecated link types (for migration tracking)
    deprecated_count = 0
    for link_type in DEPRECATED_LINK_TYPES:
        try:
            result = graph._query(f"MATCH ()-[r:{link_type}]->() RETURN count(r)")
            count = result[0][0] if result else 0
            if count > 0:
                report.total_links[f"{link_type} (DEPRECATED)"] = count
                deprecated_count += count
        except Exception as e:
            logger.warning(f"Error counting deprecated {link_type}: {e}")

    # Add warning if deprecated links exist
    if deprecated_count > 0:
        report.add_issue(Issue(
            node_type="Link",
            node_id="migration",
            issue_type="deprecated_links",
            field="type",
            message=f"{deprecated_count} deprecated link(s) found. Run migration to convert to v1.2 types.",
            severity="warning"
        ))

    return report


def validate_physics_ranges(graph: GraphOps, report: HealthReport):
    """Validate physics constraints on nodes and links.

    v1.2 constraints:
    - energy >= 0 (all nodes with energy field)
    - conductivity in [0, 1] (all links)
    - weight >= 0 (all nodes with weight field)
    - strength >= 0 (all links with strength field)
    """
    logger.info("Validating physics ranges...")

    # Check node energy >= 0
    for node_type in NODE_TYPES:
        try:
            result = graph._query(f"""
                MATCH (n:{node_type})
                WHERE n.energy IS NOT NULL AND n.energy < 0
                RETURN n.id, n.energy
            """)
            if result:
                for row in result:
                    report.add_issue(Issue(
                        node_type=node_type,
                        node_id=row[0],
                        issue_type="physics_violation",
                        field="energy",
                        message=f"Negative energy: {row[1]} (must be >= 0)",
                        severity="error"
                    ))
        except Exception as e:
            logger.warning(f"Error checking energy for {node_type}: {e}")

    # Check node weight >= 0
    for node_type in NODE_TYPES:
        try:
            result = graph._query(f"""
                MATCH (n:{node_type})
                WHERE n.weight IS NOT NULL AND n.weight < 0
                RETURN n.id, n.weight
            """)
            if result:
                for row in result:
                    report.add_issue(Issue(
                        node_type=node_type,
                        node_id=row[0],
                        issue_type="physics_violation",
                        field="weight",
                        message=f"Negative weight: {row[1]} (must be >= 0)",
                        severity="error"
                    ))
        except Exception as e:
            logger.warning(f"Error checking weight for {node_type}: {e}")

    # Check link conductivity in [0, 1]
    for link_type in ALL_LINK_TYPES:
        try:
            result = graph._query(f"""
                MATCH (a)-[r:{link_type}]->(b)
                WHERE r.conductivity IS NOT NULL AND (r.conductivity < 0 OR r.conductivity > 1)
                RETURN a.id, b.id, r.conductivity
            """)
            if result:
                for row in result:
                    report.add_issue(Issue(
                        node_type=link_type,
                        node_id=f"{row[0]}->{row[1]}",
                        issue_type="physics_violation",
                        field="conductivity",
                        message=f"Conductivity out of range: {row[2]} (must be in [0, 1])",
                        severity="error"
                    ))
        except Exception as e:
            logger.warning(f"Error checking conductivity for {link_type}: {e}")

    # Check link strength >= 0
    for link_type in ALL_LINK_TYPES:
        try:
            result = graph._query(f"""
                MATCH (a)-[r:{link_type}]->(b)
                WHERE r.strength IS NOT NULL AND r.strength < 0
                RETURN a.id, b.id, r.strength
            """)
            if result:
                for row in result:
                    report.add_issue(Issue(
                        node_type=link_type,
                        node_id=f"{row[0]}->{row[1]}",
                        issue_type="physics_violation",
                        field="strength",
                        message=f"Negative strength: {row[2]} (must be >= 0)",
                        severity="error"
                    ))
        except Exception as e:
            logger.warning(f"Error checking strength for {link_type}: {e}")


def validate_link_endpoints(graph: GraphOps, report: HealthReport):
    """Validate that all link endpoints reference existing nodes.

    This catches dangling references where node_a or node_b don't exist.
    """
    logger.info("Validating link endpoints...")

    # Check for orphaned links (endpoints with null IDs)
    for link_type in ALL_LINK_TYPES:
        try:
            # Check for links where either endpoint has null id
            result = graph._query(f"""
                MATCH (a)-[r:{link_type}]->(b)
                WHERE a.id IS NULL OR b.id IS NULL
                RETURN id(a), id(b), a.id, b.id
            """)
            if result:
                for row in result:
                    report.add_issue(Issue(
                        node_type=link_type,
                        node_id=f"internal:{row[0]}->internal:{row[1]}",
                        issue_type="orphaned_link",
                        field="endpoint",
                        message=f"Link has endpoint with null id: a.id={row[2]}, b.id={row[3]}",
                        severity="error"
                    ))
        except Exception as e:
            logger.warning(f"Error checking endpoints for {link_type}: {e}")


def validate_emotion_format(graph: GraphOps, report: HealthReport):
    """Validate emotion list format on RELATES links.

    v1.2: Emotions are stored as [[emotion_name, intensity], ...]
    - emotion_name: string
    - intensity: float in [0, 1]
    - Max 7 emotions per direction (MAX_EMOTIONS_PER_LINK)
    """
    logger.info("Validating emotion format...")

    try:
        # Check RELATES links with emotions
        result = graph._query("""
            MATCH (a)-[r:RELATES]->(b)
            WHERE r.a_emotions IS NOT NULL OR r.b_emotions IS NOT NULL
            RETURN a.id, b.id, r.a_emotions, r.b_emotions
        """)
        if result:
            for row in result:
                link_id = f"{row[0]}->{row[1]}"
                a_emotions = row[2]
                b_emotions = row[3]

                # Validate a_emotions
                if a_emotions is not None:
                    if not isinstance(a_emotions, list):
                        report.add_issue(Issue(
                            node_type="RELATES",
                            node_id=link_id,
                            issue_type="invalid_emotion_format",
                            field="a_emotions",
                            message=f"a_emotions must be a list, got {type(a_emotions).__name__}",
                            severity="error"
                        ))
                    elif len(a_emotions) > 7:
                        report.add_issue(Issue(
                            node_type="RELATES",
                            node_id=link_id,
                            issue_type="emotion_cap_exceeded",
                            field="a_emotions",
                            message=f"a_emotions has {len(a_emotions)} items (max 7)",
                            severity="warning"
                        ))

                # Validate b_emotions
                if b_emotions is not None:
                    if not isinstance(b_emotions, list):
                        report.add_issue(Issue(
                            node_type="RELATES",
                            node_id=link_id,
                            issue_type="invalid_emotion_format",
                            field="b_emotions",
                            message=f"b_emotions must be a list, got {type(b_emotions).__name__}",
                            severity="error"
                        ))
                    elif len(b_emotions) > 7:
                        report.add_issue(Issue(
                            node_type="RELATES",
                            node_id=link_id,
                            issue_type="emotion_cap_exceeded",
                            field="b_emotions",
                            message=f"b_emotions has {len(b_emotions)} items (max 7)",
                            severity="warning"
                        ))
    except Exception as e:
        logger.warning(f"Error validating emotion format: {e}")


def get_nodes_missing_field(graph: GraphOps, node_type: str, field: str) -> List[Dict]:
    """Get all nodes of a type missing a specific field."""
    cypher = f"""
    MATCH (n:{node_type})
    WHERE n.{field} IS NULL OR n.{field} = ''
    RETURN n.id as id, n.name as name
    """
    try:
        result = graph._query(cypher)
        return [{"id": row[0], "name": row[1]} for row in result] if result else []
    except Exception as e:
        logger.warning(f"Query failed for {node_type}.{field}: {e}")
        return []


def get_detailed_missing_report(graph: GraphOps, schema: Dict) -> Dict:
    """Get a detailed report of which nodes are missing which fields."""
    report = {}

    for node_type, node_schema in schema['nodes'].items():
        report[node_type] = {}

        # Check required fields
        for field in node_schema.get('required', []):
            missing = get_nodes_missing_field(graph, node_type, field)
            if missing:
                report[node_type][f"{field} (required)"] = missing

        # Check important optional fields
        important_optional = ['type', 'gender', 'alive'] if node_type == 'Actor' else []
        if node_type == 'Space':
            important_optional = ['type']
        if node_type == 'Narrative':
            important_optional = ['type', 'truth']

        for field in important_optional:
            if field in node_schema.get('optional', []):
                missing = get_nodes_missing_field(graph, node_type, field)
                if missing:
                    report[node_type][f"{field} (optional)"] = missing

    # Filter out empty entries
    return {k: v for k, v in report.items() if v}


def main():
    parser = argparse.ArgumentParser(description='Check graph health (v1.2)')
    parser.add_argument('--host', default='localhost', help='FalkorDB host')
    parser.add_argument('--port', type=int, default=6379, help='FalkorDB port')
    parser.add_argument('--graph', default='seed', help='Graph name')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--detailed', action='store_true', help='Show detailed missing field report')
    parser.add_argument('--physics', action='store_true', help='Run physics range validation')
    parser.add_argument('--endpoints', action='store_true', help='Validate link endpoints')
    parser.add_argument('--emotions', action='store_true', help='Validate emotion format')
    parser.add_argument('--all', '-a', action='store_true', help='Run all validations')
    args = parser.parse_args()

    # Connect to FalkorDB
    try:
        graph = GraphOps(graph_name=args.graph, host=args.host, port=args.port)
        logger.info(f"Connected to FalkorDB: {args.graph} at {args.host}:{args.port}")
    except Exception as e:
        logger.error(f"Cannot connect to FalkorDB: {e}")
        logger.info("Start FalkorDB with: docker run -p 6379:6379 falkordb/falkordb")
        return 1

    # Load schema
    schema = load_schema()

    # Run health check
    report = check_graph_health(graph, schema)

    # Run additional validations if requested
    if args.physics or args.all:
        validate_physics_ranges(graph, report)

    if args.endpoints or args.all:
        validate_link_endpoints(graph, report)

    if args.emotions or args.all:
        validate_emotion_format(graph, report)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        report.print_summary(verbose=args.verbose)

    # Detailed missing field report
    if args.detailed:
        print("\n--- Detailed Missing Fields Report ---\n")
        detailed = get_detailed_missing_report(graph, schema)

        if not detailed:
            print("  No missing required or important fields found.")
        else:
            for node_type, fields in detailed.items():
                print(f"\n{node_type}:")
                for field, nodes in fields.items():
                    print(f"  {field}: {len(nodes)} nodes")
                    if args.verbose:
                        for node in nodes[:5]:
                            print(f"    - {node['id']}: {node['name']}")
                        if len(nodes) > 5:
                            print(f"    ... and {len(nodes) - 5} more")

    return 0 if report.is_healthy else 1


if __name__ == "__main__":
    exit(main())

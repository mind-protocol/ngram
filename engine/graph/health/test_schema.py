#!/usr/bin/env python3
"""
Graph Engine Schema Test Suite

Verifies that the graph database matches the schema definition.
Tests node types, required fields, valid enum values, and link structures.

Usage:
    python test_schema.py [--graph NAME] [--verbose]

    pytest test_schema.py -v
"""

import json
import yaml
import pytest
from pathlib import Path
from typing import Dict, Any, List, Set, Optional
from dataclasses import dataclass, field

# Try to import FalkorDB
try:
    from falkordb import FalkorDB
    FALKORDB_AVAILABLE = True
except ImportError:
    FALKORDB_AVAILABLE = False

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
# Base schema (authoritative) - defines node_type, type as free string
BASE_SCHEMA_PATH = PROJECT_ROOT / "docs" / "schema" / "schema.yaml"
# Project-specific schema - adds Graph Engine enums
PROJECT_SCHEMA_PATH = Path(__file__).parent / "schema.yaml"


@dataclass
class SchemaViolation:
    """A schema violation found in the graph."""
    node_type: str
    node_id: str
    field: str
    issue: str
    value: Any = None


@dataclass
class TestResult:
    """Result of a schema test."""
    test_name: str
    passed: bool
    violations: List[SchemaViolation] = field(default_factory=list)
    message: str = ""


class SchemaValidator:
    """Validates graph data against schema.yaml."""

    def __init__(self, graph_name: str = "blood_ledger"):
        self.graph_name = graph_name
        self.schema = self._load_schema()
        self.graph = None
        self.results: List[TestResult] = []

        if FALKORDB_AVAILABLE:
            try:
                db = FalkorDB(host='localhost', port=6379)
                self.graph = db.select_graph(graph_name)
            except Exception as e:
                print(f"Warning: Could not connect to FalkorDB: {e}")

    def _load_schema(self) -> Dict[str, Any]:
        """Load schema.yaml.

        Loads base schema from docs/schema/schema.yaml (authoritative),
        then overlays project-specific schema for Graph Engine enums.
        """
        schema = {}

        # Load base schema (authoritative)
        if BASE_SCHEMA_PATH.exists():
            with open(BASE_SCHEMA_PATH) as f:
                schema = yaml.safe_load(f) or {}

        # Overlay project-specific schema
        if PROJECT_SCHEMA_PATH.exists():
            with open(PROJECT_SCHEMA_PATH) as f:
                project = yaml.safe_load(f) or {}
                # Merge - project schema takes precedence for validation enums
                for key, val in project.items():
                    if key not in schema:
                        schema[key] = val
                    elif isinstance(val, dict) and isinstance(schema.get(key), dict):
                        schema[key].update(val)
                    else:
                        schema[key] = val

        return schema

    def _query(self, cypher: str) -> List:
        """Run a Cypher query."""
        if not self.graph:
            return []
        try:
            result = self.graph.query(cypher)
            return result.result_set if result.result_set else []
        except Exception as e:
            print(f"Query error: {e}")
            return []

    # =========================================================================
    # NODE TESTS
    # =========================================================================

    def test_actor_required_fields(self) -> TestResult:
        """Test that all Actors have required fields (id, name)."""
        violations = []

        # Check for missing id
        rows = self._query("MATCH (c:Actor) WHERE c.id IS NULL RETURN c.name LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Actor",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing",
                value=row[0] if row else None
            ))

        # Check for missing name
        rows = self._query("MATCH (c:Actor) WHERE c.name IS NULL RETURN c.id LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Actor",
                node_id=row[0] if row else "<unknown>",
                field="name",
                issue="Required field 'name' is missing"
            ))

        return TestResult(
            test_name="Actor required fields",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} actors with missing required fields"
        )

    def test_actor_type_enum(self) -> TestResult:
        """Test that Actor.type uses valid enum values."""
        valid_types = {'player', 'companion', 'major', 'minor', 'background'}
        violations = []

        rows = self._query("""
            MATCH (c:Actor)
            WHERE c.type IS NOT NULL
            RETURN c.id, c.name, c.type
        """)

        for row in rows:
            actor_id, name, actor_type = row[0], row[1], row[2]
            if actor_type not in valid_types:
                violations.append(SchemaViolation(
                    node_type="Actor",
                    node_id=actor_id,
                    field="type",
                    issue=f"Invalid type '{actor_type}'. Valid: {valid_types}",
                    value=actor_type
                ))

        return TestResult(
            test_name="Actor type enum",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} actors with invalid type"
        )

    def test_actor_flaw_enum(self) -> TestResult:
        """Test that Actor.flaw uses valid enum values."""
        valid_flaws = {'pride', 'fear', 'greed', 'wrath', 'doubt', None}
        violations = []

        rows = self._query("""
            MATCH (c:Actor)
            WHERE c.flaw IS NOT NULL
            RETURN c.id, c.name, c.flaw
        """)

        for row in rows:
            actor_id, name, flaw = row[0], row[1], row[2]
            if flaw not in valid_flaws:
                violations.append(SchemaViolation(
                    node_type="Actor",
                    node_id=actor_id,
                    field="flaw",
                    issue=f"Invalid flaw '{flaw}'. Valid: {valid_flaws}",
                    value=flaw
                ))

        return TestResult(
            test_name="Actor flaw enum",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} actors with invalid flaw"
        )

    def test_space_required_fields(self) -> TestResult:
        """Test that all Spaces have required fields (id, name)."""
        violations = []

        rows = self._query("MATCH (p:Space) WHERE p.id IS NULL RETURN p.name LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Space",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing"
            ))

        rows = self._query("MATCH (p:Space) WHERE p.name IS NULL RETURN p.id LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Space",
                node_id=row[0] if row else "<unknown>",
                field="name",
                issue="Required field 'name' is missing"
            ))

        return TestResult(
            test_name="Space required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_space_type_enum(self) -> TestResult:
        """Test that Space.type uses valid enum values."""
        valid_types = {
            'region', 'city', 'town', 'hold', 'village', 'monastery', 'abbey',
            'crossing', 'road', 'wilderness', 'forest', 'ruin', 'camp',
            'holy_well', 'standing_stones', 'hill', 'crossroads'
        }
        violations = []

        rows = self._query("""
            MATCH (p:Space)
            WHERE p.type IS NOT NULL
            RETURN p.id, p.name, p.type
        """)

        for row in rows:
            space_id, name, space_type = row[0], row[1], row[2]
            if space_type not in valid_types:
                violations.append(SchemaViolation(
                    node_type="Space",
                    node_id=space_id,
                    field="type",
                    issue=f"Invalid type '{space_type}'",
                    value=space_type
                ))

        return TestResult(
            test_name="Space type enum",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_thing_required_fields(self) -> TestResult:
        """Test that all Things have required fields (id, name)."""
        violations = []

        rows = self._query("MATCH (t:Thing) WHERE t.id IS NULL RETURN t.name LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Thing",
                node_id="<no id>",
                field="id",
                issue="Required field 'id' is missing"
            ))

        rows = self._query("MATCH (t:Thing) WHERE t.name IS NULL RETURN t.id LIMIT 10")
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Thing",
                node_id=row[0] if row else "<unknown>",
                field="name",
                issue="Required field 'name' is missing"
            ))

        return TestResult(
            test_name="Thing required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_thing_significance_enum(self) -> TestResult:
        """Test that Thing.significance uses valid enum values."""
        valid_significance = {'mundane', 'personal', 'political', 'sacred', 'legendary'}
        violations = []

        rows = self._query("""
            MATCH (t:Thing)
            WHERE t.significance IS NOT NULL
            RETURN t.id, t.name, t.significance
        """)

        for row in rows:
            thing_id, name, sig = row[0], row[1], row[2]
            if sig not in valid_significance:
                violations.append(SchemaViolation(
                    node_type="Thing",
                    node_id=thing_id,
                    field="significance",
                    issue=f"Invalid significance '{sig}'",
                    value=sig
                ))

        return TestResult(
            test_name="Thing significance enum",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_narrative_required_fields(self) -> TestResult:
        """Test that all Narratives have required fields (id, name, content)."""
        violations = []

        for field in ['id', 'name', 'content']:
            rows = self._query(f"MATCH (n:Narrative) WHERE n.{field} IS NULL RETURN n.id, n.name LIMIT 10")
            for row in rows:
                violations.append(SchemaViolation(
                    node_type="Narrative",
                    node_id=row[0] if row and row[0] else "<unknown>",
                    field=field,
                    issue=f"Required field '{field}' is missing"
                ))

        return TestResult(
            test_name="Narrative required fields",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_narrative_type_enum(self) -> TestResult:
        """Test that Narrative.type uses valid enum values."""
        valid_types = {
            'memory', 'account', 'rumor', 'rumour', 'reputation', 'identity',
            'bond', 'oath', 'debt', 'blood', 'enmity', 'love', 'service',
            'ownership', 'claim', 'control', 'origin', 'belief', 'prophecy',
            'lie', 'secret'
        }
        violations = []

        rows = self._query("""
            MATCH (n:Narrative)
            WHERE n.type IS NOT NULL
            RETURN n.id, n.name, n.type
        """)

        for row in rows:
            narr_id, name, narr_type = row[0], row[1], row[2]
            if narr_type not in valid_types:
                violations.append(SchemaViolation(
                    node_type="Narrative",
                    node_id=narr_id,
                    field="type",
                    issue=f"Invalid type '{narr_type}'",
                    value=narr_type
                ))

        return TestResult(
            test_name="Narrative type enum",
            passed=len(violations) == 0,
            violations=violations
        )

    # =========================================================================
    # LINK TESTS
    # =========================================================================

    def test_believes_link_structure(self) -> TestResult:
        """Test that BELIEVES links go from Actor to Narrative."""
        violations = []

        # Check for BELIEVES from non-Actor
        rows = self._query("""
            MATCH (a)-[b:BELIEVES]->(n)
            WHERE NOT a:Actor
            RETURN labels(a)[0], a.id, n.id
            LIMIT 10
        """)
        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="BELIEVES",
                issue=f"BELIEVES link from {row[0]} (should be Actor)"
            ))

        # Check for BELIEVES to non-Narrative
        rows = self._query("""
            MATCH (c:Actor)-[b:BELIEVES]->(n)
            WHERE NOT n:Narrative
            RETURN c.id, labels(n)[0], n.id
            LIMIT 10
        """)
        for row in rows:
            violations.append(SchemaViolation(
                node_type="Actor",
                node_id=row[0],
                field="BELIEVES",
                issue=f"BELIEVES link to {row[1]} (should be Narrative)"
            ))

        return TestResult(
            test_name="BELIEVES link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_believes_value_ranges(self) -> TestResult:
        """Test that BELIEVES link values are within [0, 1]."""
        violations = []
        float_fields = ['heard', 'believes', 'doubts', 'denies', 'hides', 'spreads', 'originated']

        for field in float_fields:
            rows = self._query(f"""
                MATCH (c:Actor)-[b:BELIEVES]->(n:Narrative)
                WHERE b.{field} IS NOT NULL AND (b.{field} < 0 OR b.{field} > 1)
                RETURN c.id, n.id, b.{field}
                LIMIT 10
            """)
            for row in rows:
                violations.append(SchemaViolation(
                    node_type="BELIEVES",
                    node_id=f"{row[0]}->{row[1]}",
                    field=field,
                    issue=f"Value {row[2]} is outside valid range [0, 1]",
                    value=row[2]
                ))

        return TestResult(
            test_name="BELIEVES value ranges",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_at_link_structure(self) -> TestResult:
        """Test that AT links go from Actor to Space."""
        violations = []

        rows = self._query("""
            MATCH (a)-[at:AT]->(p)
            WHERE NOT a:Actor OR NOT p:Space
            RETURN labels(a)[0], a.id, labels(p)[0], p.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="AT",
                issue=f"AT link from {row[0]} to {row[2]} (should be Actor->Space)"
            ))

        return TestResult(
            test_name="AT link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_carries_link_structure(self) -> TestResult:
        """Test that CARRIES links go from Actor to Thing."""
        violations = []

        rows = self._query("""
            MATCH (a)-[r:CARRIES]->(t)
            WHERE NOT a:Actor OR NOT t:Thing
            RETURN labels(a)[0], a.id, labels(t)[0], t.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="CARRIES",
                issue=f"CARRIES link from {row[0]} to {row[2]} (should be Actor->Thing)"
            ))

        return TestResult(
            test_name="CARRIES link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_located_at_link_structure(self) -> TestResult:
        """Test that LOCATED_AT links go from Thing to Space."""
        violations = []

        rows = self._query("""
            MATCH (a)-[r:LOCATED_AT]->(p)
            WHERE NOT a:Thing OR NOT p:Space
            RETURN labels(a)[0], a.id, labels(p)[0], p.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="LOCATED_AT",
                issue=f"LOCATED_AT link from {row[0]} to {row[2]} (should be Thing->Space)"
            ))

        return TestResult(
            test_name="LOCATED_AT link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_connects_link_structure(self) -> TestResult:
        """Test that CONNECTS links go from Space to Space."""
        violations = []

        rows = self._query("""
            MATCH (a)-[r:CONNECTS]->(b)
            WHERE NOT a:Space OR NOT b:Space
            RETURN labels(a)[0], a.id, labels(b)[0], b.id
            LIMIT 10
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type=row[0],
                node_id=row[1],
                field="CONNECTS",
                issue=f"CONNECTS link from {row[0]} to {row[2]} (should be Space->Space)"
            ))

        return TestResult(
            test_name="CONNECTS link structure",
            passed=len(violations) == 0,
            violations=violations
        )

    # =========================================================================
    # DATA QUALITY TESTS
    # =========================================================================

    def test_orphan_actors(self) -> TestResult:
        """Test that actors have at least one relationship."""
        violations = []

        rows = self._query("""
            MATCH (c:Actor)
            WHERE NOT (c)-[]-()
            RETURN c.id, c.name
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Actor",
                node_id=row[0],
                field="<relationships>",
                issue="Actor has no relationships (orphan)"
            ))

        return TestResult(
            test_name="Orphan actors",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(violations)} orphan actors"
        )

    def test_actors_have_location(self) -> TestResult:
        """Test that living actors have a location (AT relationship)."""
        violations = []

        rows = self._query("""
            MATCH (c:Actor)
            WHERE (c.alive = true OR c.alive IS NULL)
            AND NOT (c)-[:AT]->(:Space)
            RETURN c.id, c.name, c.type
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Actor",
                node_id=row[0],
                field="AT",
                issue=f"Living actor '{row[1]}' has no location"
            ))

        return TestResult(
            test_name="Actors have location",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_things_have_location_or_carrier(self) -> TestResult:
        """Test that things are either at a space or carried by someone."""
        violations = []

        rows = self._query("""
            MATCH (t:Thing)
            WHERE NOT (t)-[:LOCATED_AT]->(:Space)
            AND NOT (:Actor)-[:CARRIES]->(t)
            RETURN t.id, t.name
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Thing",
                node_id=row[0],
                field="location",
                issue=f"Thing '{row[1]}' has no location and no carrier"
            ))

        return TestResult(
            test_name="Things have location or carrier",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_narratives_have_believers(self) -> TestResult:
        """Test that narratives have at least one believer."""
        violations = []

        rows = self._query("""
            MATCH (n:Narrative)
            WHERE NOT (:Actor)-[:BELIEVES]->(n)
            RETURN n.id, n.name, n.type
        """)

        for row in rows:
            violations.append(SchemaViolation(
                node_type="Narrative",
                node_id=row[0],
                field="BELIEVES",
                issue=f"Narrative '{row[1]}' has no believers"
            ))

        return TestResult(
            test_name="Narratives have believers",
            passed=len(violations) == 0,
            violations=violations
        )

    def test_player_exists(self) -> TestResult:
        """Test that exactly one player actor exists."""
        violations = []

        rows = self._query("""
            MATCH (c:Actor {type: 'player'})
            RETURN c.id, c.name
        """)

        if len(rows) == 0:
            violations.append(SchemaViolation(
                node_type="Actor",
                node_id="<none>",
                field="type",
                issue="No player actor found (type='player')"
            ))
        elif len(rows) > 1:
            for row in rows:
                violations.append(SchemaViolation(
                    node_type="Actor",
                    node_id=row[0],
                    field="type",
                    issue=f"Multiple player actors found: {row[1]}"
                ))

        return TestResult(
            test_name="Player exists",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Found {len(rows)} player actor(s)"
        )

    # =========================================================================
    # RUN ALL TESTS
    # =========================================================================

    def run_all_tests(self) -> List[TestResult]:
        """Run all schema tests."""
        if not self.graph:
            print("ERROR: No graph connection available")
            return []

        tests = [
            # Node tests
            self.test_actor_required_fields,
            self.test_actor_type_enum,
            self.test_actor_flaw_enum,
            self.test_space_required_fields,
            self.test_space_type_enum,
            self.test_thing_required_fields,
            self.test_thing_significance_enum,
            self.test_narrative_required_fields,
            self.test_narrative_type_enum,
            # Link tests
            self.test_believes_link_structure,
            self.test_believes_value_ranges,
            self.test_at_link_structure,
            self.test_carries_link_structure,
            self.test_located_at_link_structure,
            self.test_connects_link_structure,
            # Data quality tests
            self.test_orphan_actors,
            self.test_actors_have_location,
            self.test_things_have_location_or_carrier,
            self.test_narratives_have_believers,
            self.test_player_exists,
        ]

        self.results = []
        for test in tests:
            result = test()
            self.results.append(result)

        return self.results

    def print_report(self):
        """Print test results."""
        print("=" * 70)
        print("SCHEMA VALIDATION REPORT")
        print("=" * 70)
        print()

        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed

        for result in self.results:
            status = "✓" if result.passed else "✗"
            print(f"  {status} {result.test_name}")
            if not result.passed and result.violations:
                for v in result.violations[:3]:
                    print(f"      → {v.node_type}:{v.node_id} - {v.issue}")
                if len(result.violations) > 3:
                    print(f"      ... and {len(result.violations) - 3} more")

        print()
        print("=" * 70)
        print(f"PASSED: {passed}/{len(self.results)}")
        print(f"FAILED: {failed}/{len(self.results)}")
        print("=" * 70)

        return failed == 0


# =============================================================================
# PYTEST FIXTURES AND TESTS
# =============================================================================

@pytest.fixture
def validator():
    """Create a schema validator for tests."""
    return SchemaValidator()


def test_actor_required_fields(validator):
    result = validator.test_actor_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_actor_type_enum(validator):
    result = validator.test_actor_type_enum()
    assert result.passed, f"Violations: {result.violations}"


def test_space_required_fields(validator):
    result = validator.test_space_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_space_type_enum(validator):
    result = validator.test_space_type_enum()
    assert result.passed, f"Violations: {result.violations}"


def test_thing_required_fields(validator):
    result = validator.test_thing_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_narrative_required_fields(validator):
    result = validator.test_narrative_required_fields()
    assert result.passed, f"Violations: {result.violations}"


def test_narrative_type_enum(validator):
    result = validator.test_narrative_type_enum()
    assert result.passed, f"Violations: {result.violations}"


def test_believes_link_structure(validator):
    result = validator.test_believes_link_structure()
    assert result.passed, f"Violations: {result.violations}"


def test_at_link_structure(validator):
    result = validator.test_at_link_structure()
    assert result.passed, f"Violations: {result.violations}"


def test_player_exists(validator):
    result = validator.test_player_exists()
    assert result.passed, f"Violations: {result.violations}"


# =============================================================================
# CLI MAIN
# =============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate graph schema")
    parser.add_argument("--graph", default="blood_ledger", help="Graph name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    validator = SchemaValidator(graph_name=args.graph)
    validator.run_all_tests()
    success = validator.print_report()

    import sys
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

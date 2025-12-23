"""
Database migrations for FalkorDB graphs.

DOCS: docs/schema/MIGRATION_Schema_Alignment.md
"""

from .migrate_to_v2_schema import migrate_graph, migrate_all, MigrationResult

__all__ = ["migrate_graph", "migrate_all", "MigrationResult"]

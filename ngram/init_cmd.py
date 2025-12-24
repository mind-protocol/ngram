"""
Init command for ngram CLI.

Initializes the ngram in a project directory by:
- Copying protocol files to .ngram/
- Creating/updating .ngram/CLAUDE.md with inlined content (standalone)
- Creating/updating root CLAUDE.md with @ references (Claude expands these)
- Creating/updating root AGENTS.md with protocol bootstrap (inlined content)
- Creating graph named after repo and injecting seed-injection.yaml files
"""
# DOCS: docs/cli/core/PATTERNS_Why_CLI_Over_Copy.md

import shutil
import os
import re
import stat
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Any

from .core_utils import get_templates_path
from .repo_overview import generate_and_save

logger = logging.getLogger(__name__)


def _escape_marker_tokens(content: str) -> str:
    """Escape special markers so generated prompts don't trigger scanners."""
    replacements = {
        "@ngram:doctor:escalation": "@ngram&#58;doctor&#58;escalation",
        "@ngram:escalation": "@ngram&#58;escalation",
        "@ngram:doctor:proposition": "@ngram&#58;doctor&#58;proposition",
        "@ngram:proposition": "@ngram&#58;proposition",
        "@ngram:doctor:todo": "@ngram&#58;doctor&#58;todo",
        "@ngram:todo": "@ngram&#58;todo",
    }
    for source, target in replacements.items():
        content = content.replace(source, target)
    return content


def _copy_skills(skills_src: Path, target_dir: Path) -> None:
    if not skills_src.exists():
        return
    target_dir.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copytree(skills_src, target_dir, dirs_exist_ok=True)
        print(f"✓ Updated: {target_dir}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {target_dir}")


def _update_root_claude_md(target_dir: Path) -> None:
    """Update or create root CLAUDE.md with ngram section using @ references.

    If CLAUDE.md exists, replaces the '# ngram' section (or appends if not found).
    If CLAUDE.md doesn't exist, creates it with just the ngram section.
    """
    root_claude = target_dir / "CLAUDE.md"
    ngram_section = _build_root_claude_section()

    if root_claude.exists():
        content = root_claude.read_text()

        # Find and replace the ngram section
        # Look for "# ngram" heading and replace until next "# " heading or end
        pattern = r'(^# ngram\n).*?(?=^# |\Z)'

        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            # Replace existing ngram section
            new_content = re.sub(pattern, ngram_section + '\n', content, flags=re.MULTILINE | re.DOTALL)
            root_claude.write_text(new_content)
            print(f"✓ Updated ngram section in: {root_claude}")
        else:
            # Append ngram section
            new_content = content.rstrip() + '\n\n' + ngram_section
            root_claude.write_text(new_content)
            print(f"✓ Added ngram section to: {root_claude}")
    else:
        # Create new file with just ngram section
        root_claude.write_text(ngram_section)
        print(f"✓ Created: {root_claude}")


def _build_root_claude_section() -> str:
    """Build ngram section for root CLAUDE.md using @ references.

    Root CLAUDE.md uses @ references which Claude expands automatically.
    This is preferred over inlined content for the root file.
    """
    return """# ngram

@.ngram/PRINCIPLES.md

---

@.ngram/PROTOCOL.md

---

## Before Any Task

Check project state:
```
.ngram/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

## Choose Your VIEW

Based on your task, load ONE view from `.ngram/views/`:

| Task | VIEW |
|------|------|
| Processing raw data (chats, PDFs) | VIEW_Ingest_Process_Raw_Data_Sources.md |
| Getting oriented | VIEW_Onboard_Understand_Existing_Codebase.md |
| Analyzing structure | VIEW_Analyze_Structural_Analysis.md |
| Defining architecture | VIEW_Specify_Design_Vision_And_Architecture.md |
| Writing/modifying code | VIEW_Implement_Write_Or_Modify_Code.md |
| Adding features | VIEW_Extend_Add_Features_To_Existing.md |
| Pair programming | VIEW_Collaborate_Pair_Program_With_Human.md |
| Health checks | VIEW_Health_Define_Health_Checks_And_Verify.md |
| Debugging | VIEW_Debug_Investigate_And_Fix_Issues.md |
| Reviewing changes | VIEW_Review_Evaluate_Changes.md |
| Refactoring | VIEW_Refactor_Improve_Code_Structure.md |

## After Any Change

Update `.ngram/state/SYNC_Project_State.md` with what you did.
If you changed a module, update its `docs/{area}/{module}/SYNC_*.md` too.
"""


def _build_claude_addition(templates_path: Path) -> str:
    """Build CLAUDE.md content with inlined PRINCIPLES and PROTOCOL.

    Instead of using @ references (which Claude doesn't expand),
    we inline the actual content of the files.
    """
    principles_path = templates_path / "ngram" / "PRINCIPLES.md"
    protocol_path = templates_path / "ngram" / "PROTOCOL.md"

    principles_content = principles_path.read_text() if principles_path.exists() else ""
    protocol_content = protocol_path.read_text() if protocol_path.exists() else ""

    principles_content = _escape_marker_tokens(principles_content)
    protocol_content = _escape_marker_tokens(protocol_content)

    return f"""# ngram

{principles_content}

---

{protocol_content}

---

## Before Any Task

Check project state:
```
.ngram/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

## Choose Your VIEW

Based on your task, load ONE view from `.ngram/views/`:

| Task | VIEW |
|------|------|
| Processing raw data (chats, PDFs) | VIEW_Ingest_Process_Raw_Data_Sources.md |
| Getting oriented | VIEW_Onboard_Understand_Existing_Codebase.md |
| Analyzing structure | VIEW_Analyze_Structural_Analysis.md |
| Defining architecture | VIEW_Specify_Design_Vision_And_Architecture.md |
| Writing/modifying code | VIEW_Implement_Write_Or_Modify_Code.md |
| Adding features | VIEW_Extend_Add_Features_To_Existing.md |
| Pair programming | VIEW_Collaborate_Pair_Program_With_Human.md |
| Health checks | VIEW_Health_Define_Health_Checks_And_Verify.md |
| Debugging | VIEW_Debug_Investigate_And_Fix_Issues.md |
| Reviewing changes | VIEW_Review_Evaluate_Changes.md |
| Refactoring | VIEW_Refactor_Improve_Code_Structure.md |

## After Any Change

Update `.ngram/state/SYNC_Project_State.md` with what you did.
If you changed a module, update its `docs/{{area}}/{{module}}/SYNC_*.md` too.

## CLI Commands

The `ngram` command is available for project management:

```bash
ngram init [--force]    # Initialize/re-sync protocol files
ngram validate          # Check protocol invariants
ngram doctor            # Health checks (auto-archives large SYNCs)
ngram sync              # Show SYNC status (auto-archives large SYNCs)
ngram work [path] [objective]           # AI-assisted work on a path
ngram solve-markers     # Review escalations and propositions
ngram context <file>    # Get doc context for a file
ngram prompt            # Generate bootstrap prompt for LLM
ngram overview          # Generate repo map with file tree, links, definitions
ngram docs-fix          # Work doc chains and create minimal missing docs
```

### Overview Command

`ngram overview` generates a comprehensive repository map:

- File tree with character counts (respecting .gitignore/.ngramignore)
- Bidirectional links: code→docs (DOCS: markers), docs→code (references)
- Section headers from markdown, function definitions from code
- Local imports (stdlib/npm filtered out)
- Module dependencies from modules.yaml
- Output: `map.{{md|yaml|json}}` in root, plus folder-specific maps (e.g., `map_src.md`)

Options: `--dir PATH`, `--format {{md,yaml,json}}`, `--folder NAME`
"""


def _build_agents_addition(templates_path: Path) -> str:
    """Build AGENTS.md content by appending Codex-specific guidance."""
    claude_content = _build_claude_addition(templates_path)
    codex_addition_path = templates_path / "CODEX_SYSTEM_PROMPT_ADDITION.md"
    codex_addition = codex_addition_path.read_text() if codex_addition_path.exists() else ""
    if codex_addition:
        return f"{claude_content}\n\n{codex_addition}"
    return claude_content


def _build_manager_agents_addition(templates_path: Path) -> str:
    """Build manager AGENTS.md content from manager CLAUDE.md plus Codex guidance."""
    manager_claude_path = templates_path / "ngram" / "agents" / "manager" / "CLAUDE.md"
    manager_content = manager_claude_path.read_text() if manager_claude_path.exists() else ""
    codex_addition_path = templates_path / "CODEX_SYSTEM_PROMPT_ADDITION.md"
    codex_addition = codex_addition_path.read_text() if codex_addition_path.exists() else ""
    if codex_addition:
        return f"{manager_content}\n\n{codex_addition}"
    return manager_content


def _remove_write_permissions(path: Path) -> None:
    """Strip write bits so files/directories become read-only."""
    if not path.exists():
        return
    try:
        current_mode = path.stat().st_mode
        readonly_mode = current_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        path.chmod(readonly_mode)
        print(f"  ✓ Read-only: {path}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {path}")


def _enforce_readonly_for_views(views_root: Path) -> None:
    """Set view documents read-only unless they are learning artifacts."""
    if not views_root.exists():
        return
    for view_file in views_root.rglob("*.md"):
        if "LEARNING" in view_file.name.upper():
            continue
        _remove_write_permissions(view_file)


def _enforce_readonly_for_templates(templates_root: Path) -> None:
    """Set template tree to read-only so inlined source docs stay stable."""
    if not templates_root.exists():
        return
    for child in templates_root.rglob("*"):
        _remove_write_permissions(child)


# =============================================================================
# GRAPH INITIALIZATION
# =============================================================================

def _find_seed_injection_files(docs_dir: Path) -> List[Path]:
    """Find all seed-injection.yaml files in docs directory."""
    if not docs_dir.exists():
        return []

    seed_files = []
    for yaml_file in docs_dir.rglob("seed-injection.yaml"):
        seed_files.append(yaml_file)
    for yml_file in docs_dir.rglob("seed-injection.yml"):
        seed_files.append(yml_file)

    return sorted(seed_files)


def _init_graph_and_inject_seeds(target_dir: Path, clear: bool = False) -> bool:
    """
    Initialize graph named after repo and inject seed data.

    1. Get repo name from directory
    2. Connect to FalkorDB and create/select graph
    3. Optionally clear existing data (if --clear)
    4. Find all seed-injection.yaml files in docs/
    5. Upsert nodes and links from each file

    Args:
        target_dir: Project directory
        clear: If True, delete all nodes/links before injection

    Returns:
        True if successful, False if graph connection failed
    """
    repo_name = target_dir.name
    docs_dir = target_dir / "docs"

    # Find seed files first (don't need DB connection if none exist)
    seed_files = _find_seed_injection_files(docs_dir)

    print()
    print(f"Initializing graph: {repo_name}")

    try:
        from engine.physics.graph.graph_ops import GraphOps
    except ImportError as e:
        print(f"  ○ Graph init skipped (engine not available): {e}")
        return False

    try:
        graph_ops = GraphOps(graph_name=repo_name)
        print(f"  ✓ Connected to graph: {repo_name}")
    except Exception as e:
        print(f"  ○ Graph connection failed: {e}")
        print("    To enable graph features, start FalkorDB:")
        print("      docker run -p 6379:6379 falkordb/falkordb")
        return False

    # Clear graph if requested
    if clear:
        try:
            graph_ops._query("MATCH (n) DETACH DELETE n")
            print(f"  ✓ Cleared all nodes and links")
        except Exception as e:
            print(f"  ✗ Failed to clear graph: {e}")

    if not seed_files:
        print(f"  ○ No seed-injection.yaml files found in docs/")
        return True

    # Inject each seed file
    total_nodes = 0
    total_links = 0

    for seed_file in seed_files:
        print(f"  Injecting: {seed_file.relative_to(target_dir)}")

        try:
            with open(seed_file) as f:
                seed_data = yaml.safe_load(f)

            if not seed_data:
                print(f"    ○ Empty file, skipped")
                continue

            nodes = seed_data.get("nodes", [])
            links = seed_data.get("links", [])

            # Upsert nodes
            nodes_created = 0
            for node in nodes:
                try:
                    _upsert_node(graph_ops, node)
                    nodes_created += 1
                except Exception as e:
                    print(f"    ✗ Node {node.get('id', '?')}: {e}")

            # Upsert links
            links_created = 0
            for link in links:
                try:
                    _upsert_link(graph_ops, link)
                    links_created += 1
                except Exception as e:
                    print(f"    ✗ Link {link.get('id', '?')}: {e}")

            print(f"    ✓ {nodes_created} nodes, {links_created} links")
            total_nodes += nodes_created
            total_links += links_created

        except yaml.YAMLError as e:
            print(f"    ✗ Invalid YAML: {e}")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    print(f"  ✓ Total injected: {total_nodes} nodes, {total_links} links")
    return True


def _upsert_node(graph_ops, node: Dict[str, Any]) -> None:
    """Upsert a node into the graph."""
    node_id = node.get("id")
    node_type = node.get("node_type", "thing")

    if not node_id:
        raise ValueError("Node missing 'id' field")

    # Map node_type to label
    label_map = {
        "actor": "Actor",
        "space": "Space",
        "thing": "Thing",
        "narrative": "Narrative",
        "moment": "Moment",
    }
    label = label_map.get(node_type, "Thing")

    # Build properties
    props = {k: v for k, v in node.items() if k not in ("node_type",) and v is not None}

    # Handle special types
    if "content" in props and isinstance(props["content"], str):
        # Multiline content needs escaping
        props["content"] = props["content"].replace("'", "\\'").replace("\n", "\\n")

    # Build MERGE query
    props_str = ", ".join(f"{k}: ${k}" for k in props.keys())
    query = f"MERGE (n:{label} {{id: $id}}) SET n += {{{props_str}}} RETURN n.id"

    graph_ops._query(query, props)


def _upsert_link(graph_ops, link: Dict[str, Any]) -> None:
    """Upsert a link into the graph."""
    node_a = link.get("node_a")
    node_b = link.get("node_b")
    link_type = link.get("type", "relates")

    if not node_a or not node_b:
        raise ValueError("Link missing 'node_a' or 'node_b' field")

    # Map link type to relationship name
    rel_type = link_type.upper()

    # Build properties (exclude structural fields)
    exclude = {"node_a", "node_b", "type"}
    props = {k: v for k, v in link.items() if k not in exclude and v is not None}

    # Handle null values
    for k, v in list(props.items()):
        if v is None:
            del props[k]

    # Build MERGE query
    if props:
        props_str = ", ".join(f"{k}: ${k}" for k in props.keys())
        query = f"""
        MATCH (a {{id: $node_a}})
        MATCH (b {{id: $node_b}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += {{{props_str}}}
        RETURN type(r)
        """
    else:
        query = f"""
        MATCH (a {{id: $node_a}})
        MATCH (b {{id: $node_b}})
        MERGE (a)-[r:{rel_type}]->(b)
        RETURN type(r)
        """

    params = {"node_a": node_a, "node_b": node_b, **props}
    graph_ops._query(query, params)


def init_protocol(target_dir: Path, force: bool = False, clear_graph: bool = False) -> bool:
    """
    Initialize the ngram in a project directory.

    Copies protocol files and updates .ngram/CLAUDE.md and root AGENTS.md with inlined content.
    Also initializes graph and injects seed-injection.yaml files from docs/.

    Args:
        target_dir: The project directory to initialize
        force: If True, overwrite existing .ngram/
        clear_graph: If True, clear existing graph data before injection
    Returns:
        True if successful, False otherwise
    """
    try:
        templates_path = get_templates_path()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

    # Source paths
    protocol_source = templates_path / "ngram"
    modules_yaml_source = templates_path / "modules.yaml"
    ignore_source = templates_path / "ngramignore"

    # Destination paths
    protocol_dest = target_dir / ".ngram"
    modules_yaml_dest = target_dir / "modules.yaml"
    ignore_dest = target_dir / ".ngramignore"

    claude_md = protocol_dest / "CLAUDE.md"
    agents_md = target_dir / "AGENTS.md"
    manager_agents_md = protocol_dest / "agents" / "manager" / "AGENTS.md"

    # Check if already initialized
    if protocol_dest.exists() and not force:
        print(f"Error: {protocol_dest} already exists.")
        print("Use --force to overwrite.")
        return False

    # Preserve LEARNINGS files before reinitialization
    preserved_learnings = {}
    if protocol_dest.exists():
        views_dir = protocol_dest / "views"
        if views_dir.exists():
            for learnings_file in views_dir.glob("*_LEARNINGS.md"):
                content = learnings_file.read_text()
                # Only preserve if it has actual learnings (not just template)
                if "## Learnings" in content and content.count("\n") > 10:
                    preserved_learnings[learnings_file.name] = content
                    print(f"  ○ Preserving: {learnings_file.name}")
            # Also check GLOBAL_LEARNINGS.md
            global_learnings = views_dir / "GLOBAL_LEARNINGS.md"
            if global_learnings.exists():
                content = global_learnings.read_text()
                if "## Learnings" in content and content.count("\n") > 10:
                    preserved_learnings["GLOBAL_LEARNINGS.md"] = content
                    print(f"  ○ Preserving: GLOBAL_LEARNINGS.md")

    # Copy protocol files
    def copy_protocol_partial(src: Path, dst: Path) -> None:
        for root, dirs, files in os.walk(src):
            rel = Path(root).relative_to(src)
            target_root = dst / rel
            target_root.mkdir(parents=True, exist_ok=True)
            for dirname in dirs:
                (target_root / dirname).mkdir(parents=True, exist_ok=True)
            for filename in files:
                src_path = Path(root) / filename
                dst_path = target_root / filename
                try:
                    shutil.copy2(src_path, dst_path)
                except PermissionError:
                    print(f"  ○ Skipped (permission): {dst_path}")

    if protocol_dest.exists():
        try:
            shutil.rmtree(protocol_dest)
            shutil.copytree(protocol_source, protocol_dest)
            print(f"✓ Created: {protocol_dest}/")
        except PermissionError:
            print(f"  ○ Permission denied removing {protocol_dest}, attempting partial refresh")
            copy_protocol_partial(protocol_source, protocol_dest)
    else:
        shutil.copytree(protocol_source, protocol_dest)
        print(f"✓ Created: {protocol_dest}/")

    # Remove doctor-ignore after copy (we want a clean, read-only protocol install)
    doctor_ignore = protocol_dest / "doctor-ignore.yaml"
    if doctor_ignore.exists():
        try:
            doctor_ignore.unlink()
            print(f"○ Removed: {doctor_ignore}")
        except PermissionError:
            print(f"  ○ Skipped (permission): {doctor_ignore}")

    # Copy schema.yaml from docs/schema/ to .ngram/ (authoritative schema)
    schema_source = target_dir / "docs" / "schema" / "schema.yaml"
    schema_dest = protocol_dest / "schema.yaml"
    if schema_source.exists():
        try:
            shutil.copy2(schema_source, schema_dest)
            print(f"✓ Copied: {schema_dest}")
        except PermissionError:
            print(f"  ○ Skipped (permission): {schema_dest}")
    else:
        print(f"○ Schema not found: {schema_source}")

    # Restore preserved LEARNINGS files
    if preserved_learnings:
        views_dir = protocol_dest / "views"
        for filename, content in preserved_learnings.items():
            learnings_path = views_dir / filename
            try:
                learnings_path.write_text(content)
                print(f"  ✓ Restored: {filename}")
            except PermissionError:
                print(f"  ○ Skipped (permission): {learnings_path}")

    # Copy modules.yaml to project root (if not exists or force)
    if not modules_yaml_dest.exists() or force:
        if modules_yaml_source.exists():
            try:
                shutil.copy2(modules_yaml_source, modules_yaml_dest)
                print(f"✓ Created: {modules_yaml_dest}")
            except PermissionError:
                print(f"  ○ Skipped (permission): {modules_yaml_dest}")
    else:
        print(f"○ {modules_yaml_dest} already exists")

    # Copy .ngramignore to project root (if not exists or force)
    if not ignore_dest.exists() or force:
        if ignore_source.exists():
            try:
                shutil.copy2(ignore_source, ignore_dest)
                print(f"✓ Created: {ignore_dest}")
            except PermissionError:
                print(f"  ○ Skipped (permission): {ignore_dest}")
    else:
        print(f"○ {ignore_dest} already exists")

    # Copy skills into .claude/skills and Codex skills directory
    skills_src = protocol_dest / "skills"
    claude_skills_dest = target_dir / ".claude" / "skills"
    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    codex_skills_dest = codex_home / "skills"
    _copy_skills(skills_src, claude_skills_dest)
    _copy_skills(skills_src, codex_skills_dest)

    # Add agent working directories to .gitignore
    gitignore_path = target_dir / ".gitignore"
    ngram_gitignore_entries = [
        "# ngram agent working directories",
        ".ngram/agents/work/",
        ".ngram/traces/",
    ]
    try:
        existing = gitignore_path.read_text() if gitignore_path.exists() else ""
        missing_entries = [e for e in ngram_gitignore_entries if e not in existing]
        if missing_entries:
            with open(gitignore_path, "a") as f:
                f.write("\n" + "\n".join(missing_entries) + "\n")
            print(f"✓ Updated: {gitignore_path}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {gitignore_path}")

    # Build CLAUDE.md content with inlined PRINCIPLES and PROTOCOL
    # (Claude doesn't expand @ references, so we inline the actual content)
    claude_content = _build_claude_addition(templates_path)
    agents_content = _build_agents_addition(templates_path)
    manager_agents_content = _build_manager_agents_addition(templates_path)

    gemini_addition_path = templates_path / "GEMINI_SYSTEM_PROMPT_ADDITION.md"
    gemini_addition = gemini_addition_path.read_text() if gemini_addition_path.exists() else ""
    gemini_content = f"{claude_content}\n\n---\n\n{gemini_addition}" if gemini_addition else claude_content

    # Always write/overwrite CLAUDE.md with fresh inlined content
    # This ensures the latest PRINCIPLES and PROTOCOL are always included
    try:
        if claude_md.exists():
            claude_md.write_text(claude_content)
            print(f"✓ Updated: {claude_md}")
        else:
            claude_md.write_text(claude_content)
            print(f"✓ Created: {claude_md}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {claude_md}")

    # Update root CLAUDE.md with ngram section (using @ references)
    try:
        _update_root_claude_md(target_dir)
    except PermissionError:
        print(f"  ○ Skipped (permission): {target_dir / 'CLAUDE.md'}")

    gemini_md = protocol_dest / "GEMINI.md"
    try:
        gemini_md.write_text(gemini_content)
        print(f"✓ Created: {gemini_md}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {gemini_md}")

    try:
        agents_md.write_text(agents_content)
        print(f"✓ Updated: {agents_md}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {agents_md}")

    if manager_agents_content:
        try:
            manager_agents_md.parent.mkdir(parents=True, exist_ok=True)
            manager_agents_md.write_text(manager_agents_content)
            print(f"✓ Updated: {manager_agents_md}")
        except PermissionError:
            print(f"  ○ Skipped (permission): {manager_agents_md}")

    # Generate repository map
    print()
    print("Generating repository map...")
    try:
        output_path = generate_and_save(target_dir, output_format="md")
        print(f"✓ Created: {output_path}")
    except Exception as e:
        print(f"○ Map generation skipped: {e}")

    # Enforce read-only permissions for core protocol artifacts
    read_only_targets = [
        protocol_dest / "GEMINI.md",
        protocol_dest / "PRINCIPLES.md",
        protocol_dest / "PROTOCOL.md",
        protocol_dest / "schema.yaml",
        claude_md,
    ]
    for ro_path in read_only_targets:
        _remove_write_permissions(ro_path)
    _enforce_readonly_for_views(protocol_dest / "views")
    _enforce_readonly_for_templates(protocol_dest / "templates")

    # Initialize graph and inject seeds
    _init_graph_and_inject_seeds(target_dir, clear=clear_graph)

    print()
    print("ngram initialized!")
    print()
    print("Next steps:")
    print("  1. Read .ngram/PROTOCOL.md")
    print("  2. Update .ngram/state/SYNC_Project_State.md")
    print("  3. Load the VIEW matching your task when working")
    print()
    print("To bootstrap an LLM, run:")
    print(f"  ngram prompt --dir {target_dir}")

    return True

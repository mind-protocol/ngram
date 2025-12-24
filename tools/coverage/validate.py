#!/usr/bin/env python3
"""
Coverage Validation Tool

Validates that every doctor detection has a complete path to graph mutation:
Doctor Detection → Skill → Protocol(s) → Steps → Output Cluster

See docs/concepts/coverage/ for full documentation.
"""

import sys
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime


@dataclass
class Gap:
    """A coverage gap found during validation."""
    layer: str       # detection | skill | protocol | protocol_completeness | circular
    id: str          # ID of the item with the gap
    missing: str     # What's missing
    message: str     # Human-readable description


@dataclass
class CoverageResult:
    """Result of coverage validation."""
    gaps: List[Gap] = field(default_factory=list)
    total_detections: int = 0
    total_skills: int = 0
    total_protocols: int = 0
    protocols_implemented: int = 0


def load_spec(spec_path: Path) -> Optional[dict]:
    """Load and parse the coverage spec YAML."""
    try:
        with open(spec_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading spec: {e}")
        return None


def validate_detection_to_skill(spec: dict, skills_index: Dict[str, dict]) -> List[Gap]:
    """V-COV-001: Every detection must reference an existing skill."""
    gaps = []
    detections = spec.get("doctor_workflow", {}).get("detections", [])

    for detection in detections:
        skill_id = detection.get("skill")
        if skill_id not in skills_index:
            gaps.append(Gap(
                layer="detection",
                id=detection.get("id", "unknown"),
                missing=skill_id,
                message=f"Detection {detection.get('id')} references unknown skill: {skill_id}"
            ))

    return gaps


def validate_skill_to_protocol(spec: dict, protocols_index: Dict[str, dict]) -> List[Gap]:
    """V-COV-003, V-COV-004: Skills must have protocols and protocols must exist."""
    gaps = []
    skills = spec.get("skills", {})

    for skill_id, skill in skills.items():
        protocols = skill.get("protocols", [])

        # V-COV-003: No empty protocol lists
        if not protocols:
            gaps.append(Gap(
                layer="skill",
                id=skill_id,
                missing="protocols",
                message=f"Skill {skill_id} has no protocols defined"
            ))
            continue

        # V-COV-004: Protocol references must be valid
        for protocol_name in protocols:
            if protocol_name not in protocols_index:
                gaps.append(Gap(
                    layer="skill",
                    id=skill_id,
                    missing=protocol_name,
                    message=f"Skill {skill_id} references unknown protocol: {protocol_name}"
                ))

    return gaps


def validate_skill_files(spec: dict, base_path: Path) -> List[Gap]:
    """Check that skill files exist on filesystem."""
    gaps = []
    skills = spec.get("skills", {})

    for skill_id, skill in skills.items():
        file_path = base_path / skill.get("file", "")
        if not file_path.exists():
            gaps.append(Gap(
                layer="skill",
                id=skill_id,
                missing=str(skill.get("file")),
                message=f"Skill {skill_id} file missing: {skill.get('file')}"
            ))

    return gaps


def validate_protocol_files(spec: dict, base_path: Path) -> List[Gap]:
    """V-COV-005: Protocol files must exist on filesystem."""
    gaps = []
    protocols = spec.get("protocols", {})

    for protocol_name, protocol in protocols.items():
        # Skip if marked as missing in spec (we know it's not implemented)
        if protocol.get("status") == "missing":
            continue

        file_path = base_path / protocol.get("file", "")
        if not file_path.exists():
            gaps.append(Gap(
                layer="protocol",
                id=protocol_name,
                missing=str(protocol.get("file")),
                message=f"Protocol {protocol_name} file missing: {protocol.get('file')}"
            ))

    return gaps


def validate_protocol_completeness(spec: dict, base_path: Path) -> List[Gap]:
    """V-COV-006, V-COV-007: Protocols must have ask and create steps."""
    gaps = []
    protocols = spec.get("protocols", {})

    for protocol_name, protocol in protocols.items():
        if protocol.get("status") == "missing":
            continue

        file_path = base_path / protocol.get("file", "")
        if not file_path.exists():
            continue

        try:
            with open(file_path) as f:
                protocol_yaml = yaml.safe_load(f)
        except Exception:
            gaps.append(Gap(
                layer="protocol_completeness",
                id=protocol_name,
                missing="valid YAML",
                message=f"Protocol {protocol_name} has invalid YAML"
            ))
            continue

        steps = protocol_yaml.get("steps", {})
        step_types = {step.get("type") for step in steps.values() if isinstance(step, dict)}

        # V-COV-006: Must have ask
        if "ask" not in step_types:
            gaps.append(Gap(
                layer="protocol_completeness",
                id=protocol_name,
                missing="ask step",
                message=f"Protocol {protocol_name} missing required step type: ask"
            ))

        # V-COV-007: Must have create
        if "create" not in step_types:
            gaps.append(Gap(
                layer="protocol_completeness",
                id=protocol_name,
                missing="create step",
                message=f"Protocol {protocol_name} missing required step type: create"
            ))

    return gaps


def detect_circular_calls(spec: dict, base_path: Path) -> List[Gap]:
    """V-COV-009: No circular protocol calls."""
    gaps = []
    protocols = spec.get("protocols", {})

    # Build call graph
    call_graph: Dict[str, List[str]] = {}

    for protocol_name, protocol in protocols.items():
        if protocol.get("status") == "missing":
            call_graph[protocol_name] = []
            continue

        file_path = base_path / protocol.get("file", "")
        if not file_path.exists():
            call_graph[protocol_name] = []
            continue

        try:
            with open(file_path) as f:
                protocol_yaml = yaml.safe_load(f)
        except Exception:
            call_graph[protocol_name] = []
            continue

        calls = []
        for step in protocol_yaml.get("steps", {}).values():
            if not isinstance(step, dict):
                continue
            if step.get("type") == "call_protocol":
                calls.append(step.get("protocol"))
            # Check branch actions
            for check in step.get("checks", []):
                action = check.get("action", {})
                if isinstance(action, dict) and action.get("type") == "call_protocol":
                    calls.append(action.get("protocol"))

        call_graph[protocol_name] = [c for c in calls if c]

    # DFS for cycle detection
    visited: Set[str] = set()
    rec_stack: Set[str] = set()

    def dfs(node: str, path: List[str]) -> Optional[List[str]]:
        if node in rec_stack:
            cycle_start = path.index(node)
            cycle = path[cycle_start:] + [node]
            # Self-recursion is allowed (e.g., add_cluster calls itself)
            if len(cycle) == 2 and cycle[0] == cycle[1]:
                return None
            return cycle
        if node in visited:
            return None

        visited.add(node)
        rec_stack.add(node)

        for neighbor in call_graph.get(node, []):
            cycle = dfs(neighbor, path + [node])
            if cycle:
                return cycle

        rec_stack.remove(node)
        return None

    for protocol_name in call_graph:
        if protocol_name not in visited:
            cycle = dfs(protocol_name, [])
            if cycle:
                gaps.append(Gap(
                    layer="circular",
                    id=protocol_name,
                    missing="acyclic calls",
                    message=f"Circular dependency: {' → '.join(cycle)}"
                ))

    return gaps


def generate_report(result: CoverageResult, spec: dict, output_path: Path) -> None:
    """Generate markdown coverage report."""

    protocols = spec.get("protocols", {})
    implemented = sum(1 for p in protocols.values() if p.get("status") == "implemented")
    total = len(protocols)
    coverage_pct = (implemented / total * 100) if total > 0 else 0

    status = "PASS" if not result.gaps else "FAIL"
    status_icon = "✅" if not result.gaps else "❌"

    report = f"""# Coverage Validation Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

| Metric | Value |
|--------|-------|
| Total Detections | {result.total_detections} |
| Total Skills | {result.total_skills} |
| Total Protocols | {result.total_protocols} |
| Protocols Implemented | {result.protocols_implemented} |
| Coverage | {coverage_pct:.1f}% |
| Gaps | {len(result.gaps)} |

## Status

{status_icon} **{status}**{" - All paths complete" if not result.gaps else " - Gaps found"}

"""

    if result.gaps:
        report += "## Gaps\n\n"

        # Group by layer
        by_layer: Dict[str, List[Gap]] = {}
        for gap in result.gaps:
            by_layer.setdefault(gap.layer, []).append(gap)

        for layer, layer_gaps in by_layer.items():
            report += f"### {layer.replace('_', ' ').title()}\n\n"
            for gap in layer_gaps:
                report += f"- **{gap.id}**: {gap.message}\n"
            report += "\n"

    # Protocol status by phase
    report += "## Protocol Status by Phase\n\n"
    report += "| Phase | Protocol | Status | File |\n"
    report += "|-------|----------|--------|------|\n"

    for name, proto in sorted(protocols.items(), key=lambda x: (x[1].get("phase", 99), x[0])):
        phase = proto.get("phase", "?")
        status = "✅" if proto.get("status") == "implemented" else "❌"
        file = proto.get("file", "")
        report += f"| {phase} | {name} | {status} | {file} |\n"

    report += "\n"

    # Detection coverage
    report += "## Detection Coverage\n\n"
    report += "| Detection | Category | Skill | Status |\n"
    report += "|-----------|----------|-------|--------|\n"

    skills = spec.get("skills", {})
    detections = spec.get("doctor_workflow", {}).get("detections", [])

    for det in detections:
        det_id = det.get("id", "?")
        category = det.get("category", "?")
        skill_id = det.get("skill", "?")

        # Check if skill exists and has implemented protocols
        skill = skills.get(skill_id, {})
        skill_protocols = skill.get("protocols", [])
        implemented_protos = [p for p in skill_protocols if protocols.get(p, {}).get("status") == "implemented"]

        if not skill:
            status = "❌ No skill"
        elif not skill_protocols:
            status = "❌ No protocols"
        elif len(implemented_protos) == len(skill_protocols):
            status = "✅ Complete"
        else:
            status = f"🔶 Partial ({len(implemented_protos)}/{len(skill_protocols)})"

        report += f"| {det_id} | {category} | {skill_id} | {status} |\n"

    with open(output_path, "w") as f:
        f.write(report)


def validate_coverage(spec_path: Path, base_path: Path) -> CoverageResult:
    """Main validation entry point."""

    spec = load_spec(spec_path)
    if not spec:
        print("Failed to load spec")
        sys.exit(1)

    result = CoverageResult()

    # Count totals
    result.total_detections = len(spec.get("doctor_workflow", {}).get("detections", []))
    result.total_skills = len(spec.get("skills", {}))
    result.total_protocols = len(spec.get("protocols", {}))
    result.protocols_implemented = sum(
        1 for p in spec.get("protocols", {}).values()
        if p.get("status") == "implemented"
    )

    # Build indices
    skills_index = spec.get("skills", {})
    protocols_index = spec.get("protocols", {})

    # Run validations
    print("Checking detection → skill mappings...")
    result.gaps.extend(validate_detection_to_skill(spec, skills_index))

    print("Checking skill → protocol mappings...")
    result.gaps.extend(validate_skill_to_protocol(spec, protocols_index))

    print("Checking skill files exist...")
    result.gaps.extend(validate_skill_files(spec, base_path))

    print("Checking protocol files exist...")
    result.gaps.extend(validate_protocol_files(spec, base_path))

    print("Checking protocol completeness...")
    result.gaps.extend(validate_protocol_completeness(spec, base_path))

    print("Checking for circular calls...")
    result.gaps.extend(detect_circular_calls(spec, base_path))

    # Generate report
    report_path = base_path / "COVERAGE_REPORT.md"
    print(f"Generating report: {report_path}")
    generate_report(result, spec, report_path)

    return result


def main():
    # Find project root
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent.parent  # tools/coverage/validate.py -> project root
    spec_path = base_path / "specs" / "coverage.yaml"

    print(f"Coverage Validation")
    print(f"Spec: {spec_path}")
    print(f"Base: {base_path}")
    print()

    result = validate_coverage(spec_path, base_path)

    print()
    print(f"Total detections: {result.total_detections}")
    print(f"Total skills: {result.total_skills}")
    print(f"Total protocols: {result.total_protocols}")
    print(f"Protocols implemented: {result.protocols_implemented}/{result.total_protocols}")
    print(f"Gaps found: {len(result.gaps)}")
    print()

    if result.gaps:
        print("GAPS:")
        for gap in result.gaps:
            print(f"  [{gap.layer}] {gap.id}: {gap.message}")
        print()
        print("❌ FAIL - Coverage incomplete")
        sys.exit(1)
    else:
        print("✅ PASS - All paths complete")
        sys.exit(0)


if __name__ == "__main__":
    main()

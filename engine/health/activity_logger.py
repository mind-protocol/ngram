"""
Activity Logger - Two-tier logging for connectome health.

SUMMARY LOG (~500 lines):
  - Tick summaries with explanations
  - State changes (OK/WARN/ERROR)
  - Flips and interrupts
  - Aggregated stats

DETAIL LOG (~5000 lines):
  - Every node-to-node energy transfer
  - Every decay operation
  - Every link update
  - Full phase-by-phase breakdown

Logs auto-rotate when they exceed their limits.
"""

import time
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from threading import Lock


@dataclass
class LogConfig:
    summary_max_lines: int = 500
    detail_max_lines: int = 5000
    log_dir: Path = field(default_factory=lambda: Path("engine/data/logs"))


class ActivityLogger:
    """
    Two-tier activity logger with auto-rotation.

    Usage:
        logger = get_activity_logger()

        # Summary events (human-readable explanations)
        logger.tick_summary(tick=5, energy_delta=-0.7, pressure_delta=0.02)
        logger.state_change("OK", "WARN", "pressure exceeded 0.8")

        # Detail events (every operation)
        logger.energy_transfer("actor_john", "moment_talk", 0.15, "draw phase")
        logger.decay("narrative_feud", 0.95, 0.90, "5% decay rate")
    """

    def __init__(self, config: Optional[LogConfig] = None):
        self.config = config or LogConfig()
        self.config.log_dir.mkdir(parents=True, exist_ok=True)

        self.summary_path = self.config.log_dir / "health_summary.log"
        self.detail_path = self.config.log_dir / "health_detail.log"

        self._lock = Lock()
        self._summary_lines = 0
        self._detail_lines = 0

        # Count existing lines
        self._count_existing_lines()

    def _count_existing_lines(self):
        """Count lines in existing log files."""
        if self.summary_path.exists():
            self._summary_lines = sum(1 for _ in open(self.summary_path))
        if self.detail_path.exists():
            self._detail_lines = sum(1 for _ in open(self.detail_path))

    def _rotate_if_needed(self, path: Path, current_lines: int, max_lines: int) -> int:
        """Rotate log file if it exceeds max lines. Returns new line count."""
        if current_lines <= max_lines:
            return current_lines

        # Keep last half of max_lines
        keep_lines = max_lines // 2

        try:
            with open(path, 'r') as f:
                lines = f.readlines()

            # Keep only the last keep_lines
            lines = lines[-keep_lines:]

            with open(path, 'w') as f:
                f.write(f"--- LOG ROTATED at {self._ts()} (kept last {keep_lines} lines) ---\n")
                f.writelines(lines)

            return len(lines) + 1
        except Exception:
            return current_lines

    def _ts(self) -> str:
        """Timestamp for log entries."""
        return time.strftime("%H:%M:%S")

    def _write_summary(self, line: str):
        """Write to summary log with rotation."""
        with self._lock:
            self._summary_lines = self._rotate_if_needed(
                self.summary_path, self._summary_lines, self.config.summary_max_lines
            )
            with open(self.summary_path, 'a') as f:
                f.write(f"[{self._ts()}] {line}\n")
            self._summary_lines += 1

    def _write_detail(self, line: str):
        """Write to detail log with rotation."""
        with self._lock:
            self._detail_lines = self._rotate_if_needed(
                self.detail_path, self._detail_lines, self.config.detail_max_lines
            )
            with open(self.detail_path, 'a') as f:
                f.write(f"[{self._ts()}] {line}\n")
            self._detail_lines += 1

    # =========================================================================
    # SUMMARY LOG METHODS (explained, aggregated)
    # =========================================================================

    def tick_start(self, tick: int, graph_name: str = ""):
        """Log tick start."""
        self._write_summary(f"═══ TICK {tick} START ═══ graph={graph_name}")
        self._write_detail(f"═══ TICK {tick} START ═══")

    def tick_summary(
        self,
        tick: int,
        energy_before: float,
        energy_after: float,
        narratives_updated: int,
        moments_decayed: int,
        flips: int = 0
    ):
        """Log tick summary with explanation."""
        energy_delta = energy_after - energy_before

        # Build explanation
        explanation = []
        if energy_delta < 0:
            explanation.append(f"energy decayed by {abs(energy_delta):.2f}")
        elif energy_delta > 0:
            explanation.append(f"energy grew by {energy_delta:.2f}")

        exp_str = " | ".join(explanation) if explanation else "stable"

        line = (
            f"[tick:{tick}] energy {energy_before:.1f}→{energy_after:.1f} "
            f"| {exp_str}"
        )
        self._write_summary(line)

        # Also log counts
        self._write_summary(
            f"  └─ updated: {narratives_updated} narratives, "
            f"{moments_decayed} moments decayed"
        )

    def state_change(self, old_state: str, new_state: str, reason: str):
        """Log health state change with reason."""
        self._write_summary(f"⚠ STATE CHANGE: {old_state} → {new_state} | {reason}")

    def interrupt(self, reason: str, moment_id: str = ""):
        """Log an interrupt event."""
        self._write_summary(f"⏸ INTERRUPT: {reason}" + (f" moment={moment_id}" if moment_id else ""))

    def violation(self, violation_type: str, context: str = ""):
        """Log a hard invariant violation."""
        self._write_summary(f"🚨 VIOLATION: {violation_type}" + (f" | {context}" if context else ""))

    def pressure_warning(self, pressure: float, threshold: float = 0.8):
        """Log high pressure warning."""
        self._write_summary(f"⚠ HIGH PRESSURE: {pressure:.2f} > {threshold} threshold")

    # =========================================================================
    # DETAIL LOG METHODS (every operation)
    # =========================================================================

    def phase_start(self, phase: int, name: str):
        """Log phase start."""
        self._write_detail(f"── Phase {phase}: {name} ──")

    def energy_transfer(
        self,
        source_id: str,
        target_id: str,
        amount: float,
        reason: str,
        source_type: str = "",
        target_type: str = ""
    ):
        """Log energy transfer between nodes."""
        src = f"{source_type}:{source_id}" if source_type else source_id
        tgt = f"{target_type}:{target_id}" if target_type else target_id
        self._write_detail(f"  {src} ──{amount:+.3f}──> {tgt} | {reason}")

    def energy_generation(self, actor_id: str, amount: float, weight: float):
        """Log energy generation by actor."""
        self._write_detail(f"  ⚡ {actor_id} generated {amount:.3f} (weight={weight:.2f})")

    def decay(self, node_id: str, before: float, after: float, decay_rate: float, node_type: str = ""):
        """Log decay operation."""
        prefix = f"{node_type}:" if node_type else ""
        delta = after - before
        self._write_detail(
            f"  📉 {prefix}{node_id} {before:.3f}→{after:.3f} ({delta:+.3f}) rate={decay_rate:.1%}"
        )

    def link_update(
        self,
        source_id: str,
        target_id: str,
        link_type: str,
        field: str,
        old_val: float,
        new_val: float
    ):
        """Log link property update."""
        self._write_detail(
            f"  🔗 [{link_type}] {source_id}→{target_id} {field}: {old_val:.3f}→{new_val:.3f}"
        )

    def moment_draw(self, moment_id: str, actor_id: str, amount: float, conductivity: float):
        """Log moment drawing energy from actor."""
        self._write_detail(
            f"  ← {moment_id} drew {amount:.3f} from {actor_id} (cond={conductivity:.2f})"
        )

    def moment_flow(self, moment_id: str, target_id: str, amount: float, target_type: str):
        """Log moment flowing energy to target."""
        self._write_detail(
            f"  → {moment_id} flowed {amount:.3f} to {target_type}:{target_id}"
        )

    def backflow(self, narrative_id: str, actor_id: str, amount: float, belief: float):
        """Log narrative backflow to actor."""
        self._write_detail(
            f"  ↩ {narrative_id} backflowed {amount:.3f} to {actor_id} (belief={belief:.2f})"
        )

    def completion(self, moment_id: str, energy: float, tick: int):
        """Log moment completion."""
        self._write_detail(f"  ✓ COMPLETED {moment_id} energy={energy:.2f} at tick {tick}")

    def crystallization(self, actor_a: str, actor_b: str, from_moment: str, strength: float):
        """Log link crystallization between actors."""
        self._write_detail(
            f"  💎 CRYSTALLIZED {actor_a}↔{actor_b} from {from_moment} (str={strength:.2f})"
        )

    def query(self, cypher: str, result_count: int = 0):
        """Log a graph query (truncated)."""
        cypher_short = cypher.replace('\n', ' ').strip()[:80]
        self._write_detail(f"  📊 QUERY: {cypher_short}... → {result_count} results")

    def custom(self, message: str, level: str = "detail"):
        """Log custom message to appropriate log."""
        if level == "summary":
            self._write_summary(message)
        else:
            self._write_detail(message)


# Singleton
_activity_logger: Optional[ActivityLogger] = None


def get_activity_logger() -> ActivityLogger:
    """Get the global activity logger singleton."""
    global _activity_logger
    if _activity_logger is None:
        _activity_logger = ActivityLogger()
    return _activity_logger

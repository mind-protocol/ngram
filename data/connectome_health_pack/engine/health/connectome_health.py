"""Connectome Health — runtime diagnostics (stub).

Goal:
- Produce low-cost health signals by tapping existing tick diagnostics.
- Publish via SSE to connectome UI.
- Never mutate canon graph state.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Callable
import time
import math

@dataclass
class HealthStatus:
    state: str  # OK|WARN|ERROR
    score: float
    notes: List[str]

@dataclass
class InterruptInfo:
    reason: str  # spoken|active_changed|active_deactivated|contradicts_visible|none
    moment_id: Optional[str] = None
    age_ticks: Optional[int] = None

@dataclass
class RunnerInfo:
    speed: str  # pause|x1|x2|x3
    tick: int
    last_interrupt: InterruptInfo

@dataclass
class HealthCounters:
    query_write_attempts: int = 0
    dmz_violation_attempts: int = 0
    async_epoch_mismatch: int = 0

@dataclass
class AttentionStats:
    sink_set_size_p50: float = 0.0
    sink_set_size_p95: float = 0.0
    neighborhood_nodes: int = 0
    neighborhood_edges: int = 0
    focus_reconfig_rate_per_min: float = 0.0
    plateau_seconds: float = 0.0

@dataclass
class PressureStats:
    contradiction: float = 0.0
    top_edges: List[Dict[str, Any]] = None

@dataclass
class ConnectomeHealthEvent:
    ts: int
    playthrough_id: str
    place_id: str
    runner: RunnerInfo
    status: HealthStatus
    counters: HealthCounters
    attention: AttentionStats
    pressure: PressureStats

class ConnectomeHealth:
    """Sampled diagnostics aggregator.

    Integration points (recommended):
    - Called from a safe scheduler (e.g., tempo_controller tick loop) at a throttled rate.
    - Reads cached tick diagnostics collected by hot path (no heavy graph queries here).
    """
    def __init__(self, emit_every_ms: int = 500) -> None:
        self._last_emit_ms = 0
        self._emit_every_ms = emit_every_ms
        self._sink_sizes: List[int] = []
        self._focus_changes: List[int] = []
        self.counters = HealthCounters()
        self.last_interrupt = InterruptInfo(reason="none")

    def record_sink_size(self, n: int) -> None:
        self._sink_sizes.append(int(n))
        if len(self._sink_sizes) > 2000:
            self._sink_sizes = self._sink_sizes[-1000:]

    def record_focus_change(self, changed: bool) -> None:
        self._focus_changes.append(1 if changed else 0)
        if len(self._focus_changes) > 2000:
            self._focus_changes = self._focus_changes[-1000:]

    def record_interrupt(self, reason: str, moment_id: Optional[str] = None, age_ticks: Optional[int] = None) -> None:
        self.last_interrupt = InterruptInfo(reason=reason, moment_id=moment_id, age_ticks=age_ticks)

    def bump_query_write(self) -> None:
        self.counters.query_write_attempts += 1

    def bump_dmz_violation(self) -> None:
        self.counters.dmz_violation_attempts += 1

    def bump_async_epoch_mismatch(self) -> None:
        self.counters.async_epoch_mismatch += 1

    def should_emit(self) -> bool:
        now = int(time.time() * 1000)
        return (now - self._last_emit_ms) >= self._emit_every_ms

    def _pctl(self, xs: List[int], p: float) -> float:
        if not xs:
            return 0.0
        ys = sorted(xs)
        k = int(math.ceil((p / 100.0) * len(ys))) - 1
        k = max(0, min(k, len(ys) - 1))
        return float(ys[k])

    def build_event(
        self,
        playthrough_id: str,
        place_id: str,
        speed: str,
        tick: int,
        neighborhood_nodes: int,
        neighborhood_edges: int,
        contradiction_pressure: float,
        top_contradiction_edges: Optional[List[Dict[str, Any]]] = None,
        plateau_seconds: float = 0.0,
    ) -> ConnectomeHealthEvent:
        notes: List[str] = []
        state = "OK"
        score = 1.0

        if self.counters.query_write_attempts > 0 or self.counters.dmz_violation_attempts > 0:
            state = "ERROR"
            score = 0.0
            if self.counters.query_write_attempts > 0:
                notes.append("Query writes detected (must be 0).")
            if self.counters.dmz_violation_attempts > 0:
                notes.append("DMZ write attempts detected.")

        if state != "ERROR" and self.counters.async_epoch_mismatch > 0:
            state = "WARN"
            score = 0.7
            notes.append("Async epoch mismatches observed.")

        p50 = self._pctl(self._sink_sizes, 50)
        p95 = self._pctl(self._sink_sizes, 95)
        recent = self._focus_changes[-600:]  # ~ last 10 min if sampled at 1/sec; adjust later
        focus_rate = 60.0 * (sum(recent) / max(1, len(recent)))

        return ConnectomeHealthEvent(
            ts=int(time.time()),
            playthrough_id=playthrough_id,
            place_id=place_id,
            runner=RunnerInfo(speed=speed, tick=tick, last_interrupt=self.last_interrupt),
            status=HealthStatus(state=state, score=score, notes=notes),
            counters=self.counters,
            attention=AttentionStats(
                sink_set_size_p50=p50,
                sink_set_size_p95=p95,
                neighborhood_nodes=int(neighborhood_nodes),
                neighborhood_edges=int(neighborhood_edges),
                focus_reconfig_rate_per_min=float(focus_rate),
                plateau_seconds=float(plateau_seconds),
            ),
            pressure=PressureStats(
                contradiction=float(contradiction_pressure),
                top_edges=top_contradiction_edges or [],
            ),
        )

    def emit(self, event: ConnectomeHealthEvent, publish_fn: Callable[[str, Dict[str, Any]], None]) -> None:
        self._last_emit_ms = int(time.time() * 1000)
        publish_fn("connectome_health", asdict(event))

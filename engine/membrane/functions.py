from dataclasses import dataclass

from .frame import ModulationFrame


@dataclass(frozen=True)
class MembraneContext:
    tick: int
    active_density: float
    possible_density: float
    dramatic_pressure: float
    surprise_rate: float
    dominant_pressure_age: int


def clamp(value: float, low: float, high: float) -> float:
    if value < low:
        return low
    if value > high:
        return high
    return value


def activation_threshold(ctx: MembraneContext, frame: ModulationFrame) -> float:
    base = 0.6
    sparse = clamp(0.5 - ctx.active_density, -0.5, 0.5)
    base += 0.10 * sparse
    base += frame.activation_threshold_offset
    return clamp(base, 0.2, 0.9)


def weight_transfer_multiplier(ctx: MembraneContext, frame: ModulationFrame) -> float:
    base = 1.0
    if ctx.dominant_pressure_age > 20:
        base *= 1.10
    return clamp(base * frame.weight_transfer_multiplier, 0.5, 1.5)


def decay_scale(ctx: MembraneContext, frame: ModulationFrame) -> float:
    base = 1.0
    if ctx.surprise_rate < 0.05:
        base *= 1.15
    return clamp(base * frame.decay_scale, 0.5, 2.0)


def dramatic_boost_scale(ctx: MembraneContext, frame: ModulationFrame) -> float:
    base = 1.0
    if ctx.dominant_pressure_age > 20:
        base *= 1.20
    return clamp(base * frame.dramatic_boost_scale, 0.5, 2.0)

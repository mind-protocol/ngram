from dataclasses import dataclass


@dataclass(frozen=True)
class ModulationFrame:
    """Read-only modulation parameters applied during traversal/surfacing."""

    weight_transfer_multiplier: float = 1.0
    decay_scale: float = 1.0
    dramatic_boost_scale: float = 1.0
    activation_threshold_offset: float = 0.0

    @staticmethod
    def neutral() -> "ModulationFrame":
        return ModulationFrame()

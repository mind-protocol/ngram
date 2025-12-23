from engine.physics.attention_split_sink_mass_distribution_mechanism import (
    AttentionSink,
    AttentionSplitContext,
    IncomingAxisLink,
    apply_attention_split,
)
from engine.physics.contradiction_pressure_from_negative_polarity_mechanism import (
    ContradictionEdge,
    ContradictionPressureContext,
    compute_contradiction_pressure,
)
from engine.physics.primes_lag_and_half_life_decay_mechanism import (
    PrimeDecayContext,
    PrimeLink,
    compute_prime_effect,
)


def test_attention_split_conserves_budget():
    ctx = AttentionSplitContext(
        attention_temp=1.0,
        attention_scale=lambda _player_id, _place_id: 1.0,
        energy_inertia=0.2,
        sink_mass_min=0.0,
        sink_mass_max=10.0,
        softmax_epsilon=1e-8,
        role_weight=lambda _role: 1.0,
        mode_weight=lambda _mode: 1.0,
        status_weight=lambda status: 0.5 if status == "active" else 0.0,
    )
    sinks = [
        AttentionSink(
            sink_id="m1",
            sink_type="moment",
            focus=0.0,
            status="active",
            energy=0.2,
            visibility=1.0,
            incoming_links=[IncomingAxisLink(strength=1.0, role="descriptive", mode="semantic")],
        ),
        AttentionSink(
            sink_id="n1",
            sink_type="narrative",
            focus=1.5,
            status="possible",
            energy=0.0,
            visibility=1.0,
            incoming_links=[IncomingAxisLink(strength=0.8, role="descriptive", mode="semantic")],
        ),
    ]

    result = apply_attention_split("player", "place", 2.0, sinks, ctx)
    total_alloc = sum(result.allocations.values())

    assert abs(total_alloc - result.attention_budget) < 1e-6
    assert set(result.allocations.keys()) == {"m1", "n1"}
    assert result.moment_energy_next["m1"] > 0.0


def test_primes_lag_and_half_life():
    link = PrimeLink(
        link_id="p1",
        source_id="a",
        target_id="b",
        strength=0.6,
        lag_ticks=2,
        half_life_ticks=2.0,
        intent_tags=["pacing"],
        source_tick_created=0,
    )

    early = compute_prime_effect(link, PrimeDecayContext(
        current_tick=1,
        half_life_floor=0.1,
        strength_min=0.0,
        strength_max=1.0,
    ))
    assert early.effect == 0.0

    on_lag = compute_prime_effect(link, PrimeDecayContext(
        current_tick=2,
        half_life_floor=0.1,
        strength_min=0.0,
        strength_max=1.0,
    ))
    assert abs(on_lag.effect - 0.6) < 1e-6

    later = compute_prime_effect(link, PrimeDecayContext(
        current_tick=4,
        half_life_floor=0.1,
        strength_min=0.0,
        strength_max=1.0,
    ))
    assert abs(later.effect - 0.3) < 1e-6


def test_contradiction_pressure_accumulates_and_decays():
    edges = [
        ContradictionEdge(
            edge_id="e1",
            source_id="n1",
            target_id="n2",
            polarity=-0.5,
            strength=0.8,
            confidence=0.5,
        ),
        ContradictionEdge(
            edge_id="e2",
            source_id="n2",
            target_id="n3",
            polarity=0.4,
            strength=1.0,
            confidence=1.0,
        ),
    ]
    ctx = ContradictionPressureContext(
        contradiction_gain=1.0,
        pressure_decay=0.5,
        pressure_min=0.0,
        pressure_max=1.0,
    )

    result = compute_contradiction_pressure(edges, ctx, previous_pressure=0.1)
    assert abs(result.pressure - 0.2) < 1e-6
    assert abs(result.pressure_next - 0.25) < 1e-6
    assert len(result.contributions) == 1

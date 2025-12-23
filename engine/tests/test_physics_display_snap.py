from __future__ import annotations

import pytest

from engine.physics.display_snap_transition_checker import (
    SnapDisplayState,
    SnapMomentContext,
    SnapPhase,
    execute_snap,
    should_display,
)


def test_snap_only_triggers_on_interrupts():
    moment = SnapMomentContext(references={'player'}, dramatic_pressure=0.95)
    state = SnapDisplayState(speed='3x')

    assert should_display(moment, '3x')
    phases = execute_snap(moment, state)

    assert state.speed == '1x'
    assert [phase.phase for phase in phases] == [
        SnapPhase.RUNNING,
        SnapPhase.BEAT,
        SnapPhase.ARRIVAL,
    ]
    assert 0.3 <= phases[1].duration <= 0.5
    assert 'crystal clear' not in phases[1].description.lower()


def test_snap_rejects_non_interrupt():
    state = SnapDisplayState(speed='3x')
    passive = SnapMomentContext(weight=0.2, references=set())

    assert not should_display(passive, '3x')
    with pytest.raises(ValueError):
        execute_snap(passive, state)


def test_display_filters_at_two_x():
    dialogue = SnapMomentContext(type='dialogue', weight=0.35)
    montage = SnapMomentContext(type='montage', weight=0.45)

    assert should_display(dialogue, '2x')
    assert should_display(montage, '2x')

    montage.weight = 0.3
    assert not should_display(montage, '2x')

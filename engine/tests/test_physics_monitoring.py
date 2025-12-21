from engine.physics.monitoring import (
    DisplaySnapshot,
    detect_cluster_surges,
    summarize_cluster_energy,
    validate_snap_transition,
)


def test_validate_snap_transition_success():
    frames = [
        DisplaySnapshot(speed="3x", visual_style="motion blur", text_flow="streaming"),
        DisplaySnapshot(speed="3x", visual_style="freeze", text_flow="streaming", silence_ms=400),
        DisplaySnapshot(speed="1x", visual_style="full clarity", text_flow="centered"),
    ]

    result = validate_snap_transition(frames)

    assert result.is_valid
    assert result.reasons == []


def test_validate_snap_transition_fails_when_missing_beat():
    frames = [
        DisplaySnapshot(speed="3x", visual_style="motion blur", text_flow="streaming"),
        DisplaySnapshot(speed="3x", visual_style="running", text_flow="streaming"),
        DisplaySnapshot(speed="1x", visual_style="full clarity", text_flow="centered"),
    ]

    result = validate_snap_transition(frames)

    assert not result.is_valid
    assert any("silence" in reason.lower() for reason in result.reasons)


def test_summarize_cluster_energy_and_detect_surges():
    nodes = [
        {"id": "n1", "cluster_id": "alpha", "energy": 30},
        {"id": "n2", "cluster_id": "alpha", "energy": 20},
        {"id": "n3", "cluster_id": "beta", "energy": 10},
    ]

    clusters = summarize_cluster_energy(nodes)

    assert clusters["alpha"].total_energy == 50
    assert clusters["alpha"].node_count == 2
    assert clusters["alpha"].average_energy == 25
    assert clusters["beta"].total_energy == 10

    surges = detect_cluster_surges(clusters, surge_multiplier=1.2)
    assert "alpha" in surges
    assert "beta" not in surges


def test_detect_cluster_surges_returns_empty_for_no_data():
    assert detect_cluster_surges({}) == []

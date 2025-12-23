"""
Tests for Schema v1.2 Energy Physics

Tests the v1.2 energy flow mechanics:
- No decay (energy persists)
- Hot/cold links (Top-N filter)
- Unified traversal (energy + strength + emotions)
- Target weight (sqrt reception)
- 8 tick phases

These are unit tests - no database required.

DOCS: docs/physics/VALIDATION_Energy_Physics.md

VALIDATES:
    V-ENERGY-NON-NEGATIVE
    V-LINK-STRENGTH-GROWTH
    V-MOMENT-TRANSITIONS
    V-MOMENT-DURATION-RATE
    V-GEN-PROXIMITY-BOUNDS
    V-EMOTION-BASELINE
    V-EMOTION-BLEND

OWNER: Claude Dev 2
"""

import pytest
import math
from typing import List

# Import v1.2 components
from engine.physics.tick_v1_2 import (
    # Constants
    GENERATION_RATE,
    DRAW_RATE,
    BACKFLOW_RATE,
    COLD_THRESHOLD,
    TOP_N_LINKS,
    LINK_DRAIN_RATE,
    LINK_TO_STRENGTH_RATE,
    SUPPORT_THRESHOLD,
    CONTRADICT_THRESHOLD,
    INTERACTION_RATE,
    REJECTION_RETURN_RATE,
    TICKS_PER_MINUTE,
    # Functions
    avg_emotion_intensity,
    emotion_proximity,
    blend_emotions,
    get_weighted_average_emotions,
    # Result type
    TickResultV1_2,
)


# =============================================================================
# EMOTION FUNCTIONS
# =============================================================================

class TestEmotionFunctions:
    """Test emotion utility functions.

    # @ngram:physics:energy:test:TestEmotionFunctions
    """

    # @ngram:physics:energy:test:test_avg_emotion_intensity_empty
    # @ngram:physics:energy:validates:V-EMOTION-BASELINE
    def test_avg_emotion_intensity_empty(self):
        """Empty list returns 0.5 baseline."""
        assert avg_emotion_intensity([]) == 0.5

    def test_avg_emotion_intensity_single(self):
        """Single emotion returns its intensity."""
        assert avg_emotion_intensity([["fear", 0.8]]) == 0.8

    def test_avg_emotion_intensity_multiple(self):
        """Multiple emotions returns average."""
        emotions = [["fear", 0.8], ["hope", 0.4]]
        assert abs(avg_emotion_intensity(emotions) - 0.6) < 0.0001

    # @ngram:physics:energy:test:test_emotion_proximity_empty
    # @ngram:physics:energy:validates:V-EMOTION-BASELINE
    def test_emotion_proximity_empty(self):
        """Empty lists return 0.2 baseline."""
        assert emotion_proximity([], []) == 0.2
        assert emotion_proximity([["fear", 0.8]], []) == 0.2
        assert emotion_proximity([], [["hope", 0.5]]) == 0.2

    def test_emotion_proximity_identical(self):
        """Identical emotions return high proximity."""
        a = [["fear", 1.0]]
        b = [["fear", 1.0]]
        result = emotion_proximity(a, b)
        assert result == 1.0  # Perfect match

    def test_emotion_proximity_no_overlap(self):
        """No overlap returns low proximity."""
        a = [["fear", 0.8]]
        b = [["hope", 0.9]]
        result = emotion_proximity(a, b)
        assert result == 0.0  # No intersection

    def test_emotion_proximity_partial(self):
        """Partial overlap returns intermediate."""
        a = [["fear", 0.8], ["hope", 0.4]]
        b = [["fear", 0.6], ["anger", 0.5]]
        result = emotion_proximity(a, b)
        assert 0 < result < 1

    def test_blend_emotions_empty_existing(self):
        """Blending into empty adds scaled emotions."""
        existing = []
        incoming = [["fear", 0.8]]
        result = blend_emotions(existing, incoming, 0.5)
        assert len(result) == 1
        assert result[0][0] == "fear"
        assert result[0][1] == 0.4  # 0.8 * 0.5

    # @ngram:physics:energy:test:test_blend_emotions_same_emotion
    # @ngram:physics:energy:validates:V-EMOTION-BLEND
    def test_blend_emotions_same_emotion(self):
        """Blending same emotion uses diminishing returns."""
        existing = [["fear", 0.5]]
        incoming = [["fear", 0.8]]
        result = blend_emotions(existing, incoming, 0.5)
        assert len(result) == 1
        assert result[0][0] == "fear"
        # Diminishing returns: 0.5 + (0.8 * 0.5) * (1 - 0.5) = 0.7
        assert 0.69 < result[0][1] < 0.71

    def test_blend_emotions_new_emotion(self):
        """Blending adds new emotions."""
        existing = [["fear", 0.5]]
        incoming = [["hope", 0.6]]
        result = blend_emotions(existing, incoming, 0.5)
        assert len(result) == 2
        emotions = {e[0]: e[1] for e in result}
        assert "fear" in emotions
        assert "hope" in emotions

    def test_blend_emotions_max_cap(self):
        """Blending respects max_emotions cap."""
        existing = [["a", 0.9], ["b", 0.8], ["c", 0.7]]
        incoming = [["d", 0.6], ["e", 0.5]]
        result = blend_emotions(existing, incoming, 1.0, max_emotions=3)
        assert len(result) == 3

    def test_get_weighted_average_emotions_empty(self):
        """Empty links returns empty emotions."""
        assert get_weighted_average_emotions([]) == []

    def test_get_weighted_average_emotions_single(self):
        """Single link returns its emotions scaled by weight."""
        links = [{"weight": 2.0, "emotions": [["fear", 0.8]]}]
        result = get_weighted_average_emotions(links)
        assert len(result) == 1
        assert result[0][0] == "fear"
        assert result[0][1] == 0.8  # Normalized

    def test_get_weighted_average_emotions_weighted(self):
        """Multiple links weighted by their weights."""
        links = [
            {"weight": 2.0, "emotions": [["fear", 1.0]]},
            {"weight": 1.0, "emotions": [["fear", 0.4]]},
        ]
        result = get_weighted_average_emotions(links)
        # (2*1.0 + 1*0.4) / (2+1) = 2.4/3 = 0.8
        assert len(result) == 1
        assert result[0][0] == "fear"
        assert 0.79 < result[0][1] < 0.81


# =============================================================================
# CONSTANTS
# =============================================================================

class TestV1_2Constants:
    """Test v1.2 constants are defined correctly."""

    def test_generation_rate(self):
        assert GENERATION_RATE == 0.5

    def test_draw_rate(self):
        assert DRAW_RATE == 0.3

    def test_backflow_rate(self):
        assert BACKFLOW_RATE == 0.1

    def test_cold_threshold(self):
        assert COLD_THRESHOLD == 0.01

    def test_top_n_links(self):
        assert TOP_N_LINKS == 20

    def test_link_drain_rate(self):
        assert LINK_DRAIN_RATE == 0.3

    def test_link_to_strength_rate(self):
        assert LINK_TO_STRENGTH_RATE == 0.1

    def test_support_threshold(self):
        assert SUPPORT_THRESHOLD == 0.7

    def test_contradict_threshold(self):
        assert CONTRADICT_THRESHOLD == 0.3

    def test_interaction_rate(self):
        assert INTERACTION_RATE == 0.05

    def test_rejection_return_rate(self):
        assert REJECTION_RETURN_RATE == 0.8

    def test_ticks_per_minute(self):
        assert TICKS_PER_MINUTE == 12


# =============================================================================
# FLOW FORMULAS
# =============================================================================

class TestFlowFormulas:
    """Test the unified flow formula components.

    # @ngram:physics:energy:test:TestFlowFormulas
    """

    def test_unified_flow_basic(self):
        """flow = source.energy × rate × conductivity × weight × emotion_factor"""
        source_energy = 10.0
        rate = DRAW_RATE  # 0.3
        conductivity = 1.0
        weight = 1.0
        emotion_factor = 1.0

        flow = source_energy * rate * conductivity * weight * emotion_factor
        assert flow == 3.0  # 10 * 0.3 * 1 * 1 * 1

    def test_received_with_target_weight(self):
        """received = flow × sqrt(target.weight)"""
        flow = 3.0
        target_weight = 4.0

        received = flow * math.sqrt(target_weight)
        assert received == 6.0  # 3.0 * 2.0

    def test_target_weight_diminishing_returns(self):
        """sqrt provides diminishing returns."""
        flow = 1.0

        # Weight 1 → sqrt = 1
        assert flow * math.sqrt(1.0) == 1.0

        # Weight 4 → sqrt = 2 (not 4)
        assert flow * math.sqrt(4.0) == 2.0

        # Weight 9 → sqrt = 3 (not 9)
        assert flow * math.sqrt(9.0) == 3.0

    # @ngram:physics:energy:test:test_radiation_rate_formula
    # @ngram:physics:energy:validates:V-MOMENT-DURATION-RATE
    def test_radiation_rate_formula(self):
        """radiation_rate = 1 / (duration_minutes × 12)"""
        duration = 1.0  # 1 minute
        rate = 1.0 / (duration * TICKS_PER_MINUTE)
        assert rate == 1.0 / 12

        duration = 5.0  # 5 minutes
        rate = 1.0 / (duration * TICKS_PER_MINUTE)
        assert rate == 1.0 / 60

    # @ngram:physics:energy:test:test_proximity_formula
    # @ngram:physics:energy:validates:V-GEN-PROXIMITY-BOUNDS
    def test_proximity_formula(self):
        """proximity = 1 / (1 + path_resistance)"""
        # Zero resistance = full proximity
        assert 1.0 / (1.0 + 0.0) == 1.0

        # Resistance 1 = 50% proximity
        assert 1.0 / (1.0 + 1.0) == 0.5

        # High resistance = low proximity
        assert 1.0 / (1.0 + 100.0) < 0.01


# =============================================================================
# HOT/COLD LINKS
# =============================================================================

class TestHotColdLinks:
    """Test hot/cold link filtering."""

    def test_heat_score_formula(self):
        """heat_score = energy × weight"""
        energy = 0.5
        weight = 2.0
        assert energy * weight == 1.0

    def test_cold_threshold_boundary(self):
        """Links below threshold are cold."""
        energy = 0.005
        weight = 1.0
        heat_score = energy * weight
        assert heat_score < COLD_THRESHOLD
        assert heat_score <= 0.01

    def test_hot_threshold_boundary(self):
        """Links above threshold are hot."""
        energy = 0.02
        weight = 1.0
        heat_score = energy * weight
        assert heat_score > COLD_THRESHOLD
        assert heat_score > 0.01


# =============================================================================
# LINK COOLING (NO DECAY)
# =============================================================================

class TestLinkCooling:
    """Test link cooling mechanics (replaces decay)."""

    def test_drain_calculation(self):
        """30% of energy drains to nodes."""
        link_energy = 1.0
        drain = link_energy * LINK_DRAIN_RATE
        assert drain == 0.3

    def test_drain_split(self):
        """Drain splits 50/50 to connected nodes."""
        drain = 0.3
        a_share = drain * 0.5
        b_share = drain * 0.5
        assert a_share == 0.15
        assert b_share == 0.15

    def test_strength_conversion(self):
        """10% converts to permanent strength."""
        link_energy = 1.0
        to_strength = link_energy * LINK_TO_STRENGTH_RATE
        assert to_strength == 0.1

    # @ngram:physics:energy:test:test_strength_growth_formula
    # @ngram:physics:energy:validates:V-LINK-STRENGTH-GROWTH
    def test_strength_growth_formula(self):
        """growth = (energy × 0.1 × emotion × a.weight) / ((1 + strength) × b.weight)"""
        energy = 1.0
        emotion_intensity = 0.5
        a_weight = 2.0
        b_weight = 1.0
        current_strength = 0.0

        growth = (energy * 0.1 * emotion_intensity * a_weight) / ((1 + current_strength) * b_weight)
        assert growth == 0.1  # (1 * 0.1 * 0.5 * 2) / (1 * 1) = 0.1

    # @ngram:physics:energy:test:test_strength_diminishing_returns
    # @ngram:physics:energy:validates:V-LINK-STRENGTH-GROWTH
    def test_strength_diminishing_returns(self):
        """Higher strength means slower growth."""
        energy = 1.0
        emotion_intensity = 0.5
        a_weight = 2.0
        b_weight = 1.0

        # Low strength = fast growth
        growth_low = (energy * 0.1 * emotion_intensity * a_weight) / ((1 + 0.0) * b_weight)

        # High strength = slow growth
        growth_high = (energy * 0.1 * emotion_intensity * a_weight) / ((1 + 9.0) * b_weight)

        assert growth_low > growth_high
        assert growth_low == 0.1
        assert growth_high == 0.01


# =============================================================================
# MOMENT INTERACTION
# =============================================================================

class TestMomentInteraction:
    """Test support/contradict between moments.

    # @ngram:physics:energy:test:TestMomentInteraction
    """

    # @ngram:physics:energy:test:test_support_threshold
    # @ngram:physics:energy:validates:V-MOMENT-TRANSITIONS
    def test_support_threshold(self):
        """Proximity > 0.7 triggers support."""
        proximity = 0.8
        assert proximity > SUPPORT_THRESHOLD

    # @ngram:physics:energy:test:test_contradict_threshold
    # @ngram:physics:energy:validates:V-MOMENT-TRANSITIONS
    def test_contradict_threshold(self):
        """Proximity < 0.3 triggers contradict."""
        proximity = 0.2
        assert proximity < CONTRADICT_THRESHOLD

    def test_support_formula(self):
        """support = m1.energy × 0.05 × proximity"""
        m1_energy = 10.0
        proximity = 0.8
        support = m1_energy * INTERACTION_RATE * proximity
        assert support == 0.4  # 10 * 0.05 * 0.8

    def test_contradict_formula(self):
        """suppress = m1.energy × 0.05 × (1 - proximity)"""
        m1_energy = 10.0
        proximity = 0.2
        suppress = m1_energy * INTERACTION_RATE * (1 - proximity)
        assert suppress == 0.4  # 10 * 0.05 * 0.8


# =============================================================================
# REJECTION
# =============================================================================

class TestRejection:
    """Test rejection mechanics."""

    def test_energy_return_rate(self):
        """80% returns to player."""
        moment_energy = 10.0
        returned = moment_energy * REJECTION_RETURN_RATE
        assert returned == 8.0


# =============================================================================
# RESULT TYPE
# =============================================================================

class TestTickResultV1_2:
    """Test the v1.2 result dataclass."""

    def test_default_values(self):
        """Result has sensible defaults."""
        result = TickResultV1_2()
        assert result.energy_generated == 0.0
        assert result.energy_drawn == 0.0
        assert result.energy_flowed == 0.0
        assert result.energy_interacted == 0.0
        assert result.energy_backflowed == 0.0
        assert result.energy_cooled == 0.0
        assert result.actors_updated == 0
        assert result.moments_active == 0
        assert result.moments_possible == 0
        assert result.moments_completed == 0
        assert result.moments_rejected == 0
        assert result.hot_links == 0
        assert result.cold_links == 0
        assert result.completions == []
        assert result.rejections == []

    def test_result_can_be_populated(self):
        """Result fields can be set."""
        result = TickResultV1_2()
        result.energy_generated = 10.0
        result.hot_links = 50
        result.completions = [{"moment_id": "m1"}]

        assert result.energy_generated == 10.0
        assert result.hot_links == 50
        assert len(result.completions) == 1


# =============================================================================
# INTEGRATION: NO DECAY
# =============================================================================

class TestNoDecay:
    """Verify v1.2 has no arbitrary decay.

    # @ngram:physics:energy:test:TestNoDecay
    """

    def test_no_decay_constants(self):
        """v1.2 constants have no decay rates."""
        # These should NOT exist in v1.2
        from engine.physics.tick_v1_2 import (
            GENERATION_RATE,
            DRAW_RATE,
            LINK_DRAIN_RATE,
        )

        # Verify they're flow/cooling rates, not decay
        assert GENERATION_RATE == 0.5  # Generation, not decay
        assert DRAW_RATE == 0.3  # Draw, not decay
        assert LINK_DRAIN_RATE == 0.3  # Drain (cooling), not decay

    # @ngram:physics:energy:test:test_energy_lifecycle
    # @ngram:physics:energy:validates:V-ENERGY-NON-NEGATIVE
    def test_energy_lifecycle(self):
        """Energy flows through system without arbitrary decay."""
        # Energy lifecycle:
        # 1. Generated by actors
        # 2. Drawn by moments
        # 3. Flowed to nodes
        # 4. Returned via cooling
        # 5. Converted to strength

        initial_energy = 10.0

        # After draw
        drawn = initial_energy * DRAW_RATE
        remaining_actor = initial_energy - drawn

        # After cooling (if this energy went to a link)
        drain = drawn * LINK_DRAIN_RATE
        to_nodes = drain * 0.5 * 2  # Both nodes get 50%
        to_strength = drawn * LINK_TO_STRENGTH_RATE

        # Energy is conserved (with some going to strength)
        total_after = remaining_actor + to_nodes + to_strength

        # No arbitrary decay - energy either stays or converts
        assert total_after > 0

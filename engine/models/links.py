"""
Link Models — Generic Schema Types

The link types that connect nodes.
Based on schema.yaml v1.2

v1.2 CHANGES:
    - Added link types: about (Moment → Any), attached_to (Thing → Actor/Space)
    - Added LinkDirection enum: support, oppose, elaborate, subsume, supersede
    - Added semantic properties: name, role, direction, description
    - energy: current attention (hot/cold filter) — NO DECAY
    - strength: accumulated depth (permanent, grows with traversal)
    - Link cooling: 30% drain to nodes, 10% converts to strength
    - Migration: 14 old types → 9 new types (old types become property values)

v1.1 CHANGES:
    - Added LinkType enum: contains, leads_to, expresses, sequence, primes, can_become, relates
    - Added LinkBase with unified fields: node_a, node_b, conductivity, weight, energy, strength, emotions
    - emotions: Hebbian-colored by energy flow ([[name, intensity], ...])
    - Bidirectional: node_a/node_b replaces from_id/to_id

MIGRATION (legacy → v1.2):
    BELIEVES → relates + role:believer
    ORIGINATED → relates + role:originator
    SUPPORTS → relates + direction:support
    CONTRADICTS → relates + direction:oppose
    WITNESSED → relates + role:witness
    OWES → relates + role:debtor + name:'owes debt to'
    CAN_SPEAK/SAID → expresses
    AT → contains (inverted)
    CARRIES → attached_to (inverted)

TESTS:
    engine/tests/test_models.py::TestActorNarrativeLink
    engine/tests/test_models.py::TestNarrativeNarrativeLink

SEE ALSO:
    docs/schema/schema.yaml
"""

from typing import Optional, List, Tuple
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .base import BeliefSource, PathDifficulty


# =============================================================================
# LINK TYPE ENUM (v1.1)
# =============================================================================

class LinkType(str, Enum):
    """The 9 link types in schema v1.2.

    Taxonomy:
        Energy carriers: expresses, about, relates, attached_to
        Structural only: contains, leads_to, sequence, primes, can_become

    Migration from legacy types:
        BELIEVES, ORIGINATED, SUPPORTS, CONTRADICTS, ELABORATES → relates
        CAN_SPEAK, SAID → expresses
        ATTACHED_TO (moment) → about
        CARRIES → attached_to (inverted)
        AT → contains (inverted)
        THEN → sequence
        CAN_LEAD_TO → primes
    """
    # Energy carriers (participate in physics tick)
    EXPRESSES = "expresses"      # Actor → Moment (draw phase)
    ABOUT = "about"              # Moment → Any (flow phase)
    ATTACHED_TO = "attached_to"  # Thing → Actor/Space (flow phase)
    RELATES = "relates"          # Any → Any (flow, backflow)

    # Structural (no energy flow)
    CONTAINS = "contains"      # Space → Actor/Thing/Space (hierarchy)
    LEADS_TO = "leads_to"      # Space → Space (path)
    SEQUENCE = "sequence"      # Moment → Moment (history)
    PRIMES = "primes"          # Moment → Moment (traversal possibility)
    CAN_BECOME = "can_become"  # Thing → Thing (transformation)


class LinkDirection(str, Enum):
    """Semantic direction for relates links (v1.2).

    Replaces old type differentiation:
        SUPPORTS → direction: support
        CONTRADICTS → direction: oppose
        ELABORATES → direction: elaborate
        SUBSUMES → direction: subsume
        SUPERSEDES → direction: supersede
    """
    SUPPORT = "support"       # Reinforces, aligns with
    OPPOSE = "oppose"         # Contradicts, conflicts with
    ELABORATE = "elaborate"   # Adds detail to
    SUBSUME = "subsume"       # Is a specific case of
    SUPERSEDE = "supersede"   # Replaces, obsoletes


# =============================================================================
# LINK BASE (v1.2)
# =============================================================================

class LinkBase(BaseModel):
    """Unified link model for schema v1.2.

    All links have:
        - node_a, node_b: bidirectional endpoints
        - type: one of the 9 LinkTypes
        - conductivity: percentage of energy that passes through [0-1]
        - weight: link importance (unbounded)
        - energy: current attention (hot/cold filter) — NO DECAY
        - strength: accumulated depth (permanent, grows with each traversal)
        - emotions: Hebbian-colored by energy flow
        - name: link label (e.g., 'believes', 'owes debt to')
        - role: semantic role (originator, believer, witness, subject, creditor, debtor)
        - direction: semantic direction (support, oppose, elaborate, subsume, supersede)
        - description: human-readable description

    Hot vs Cold:
        link.energy × link.weight > COLD_THRESHOLD → HOT → in physics
        link.energy × link.weight ≤ COLD_THRESHOLD → COLD → excluded

    Link Cooling (per tick):
        - 30% of energy drains to connected nodes (50/50 split)
        - 10% of energy converts to permanent strength
        - No arbitrary decay

    Semantic Differentiation (v1.2):
        Instead of 14+ link types, use 9 types + semantic properties:
        - BELIEVES → relates + role:believer
        - ORIGINATED → relates + role:originator + higher weight
        - SUPPORTS → relates + direction:support + emotions:[[alignment, X]]
        - CONTRADICTS → relates + direction:oppose + emotions:[[opposition, X]]
        - WITNESSED → relates + role:witness
        - OWES → relates + role:debtor + name:'owes debt to'
    """
    # Endpoints (bidirectional)
    node_a: str = Field(description="First node ID")
    node_b: str = Field(description="Second node ID")

    # Type
    type: LinkType = Field(default=LinkType.RELATES, description="Link type")

    # Physics (v1.2)
    conductivity: float = Field(
        default=1.0, ge=0.0, le=1.0,
        description="Percentage of energy that passes through"
    )
    weight: float = Field(
        default=1.0, ge=0.0,
        description="Link importance (unbounded)"
    )
    energy: float = Field(
        default=0.0, ge=0.0,
        description="Current attention (hot/cold filter, no decay)"
    )
    strength: float = Field(
        default=0.0, ge=0.0,
        description="Accumulated depth (permanent, grows with traversal)"
    )

    # Emotions (Hebbian-colored by energy flow)
    emotions: List[List] = Field(
        default_factory=list,
        description="[[name, intensity], ...] — colored by what flows through"
    )

    # Semantic properties (v1.2)
    name: str = Field(
        default="",
        description="Link name/label (e.g., 'believes', 'owes debt to', 'witnessed')"
    )
    role: Optional[str] = Field(
        default=None,
        description="Semantic role: originator, believer, witness, subject, creditor, debtor"
    )
    direction: Optional[LinkDirection] = Field(
        default=None,
        description="Semantic direction: support, oppose, elaborate, subsume, supersede"
    )
    description: str = Field(
        default="",
        description="Human-readable description of the link"
    )
    created_at_s: int = Field(
        default=0, ge=0,
        description="Unix timestamp when link was created"
    )

    @property
    def heat_score(self) -> float:
        """Calculate heat score for top-N filtering.

        v1.2: score = energy × weight
        """
        return self.energy * self.weight

    def is_hot(self, threshold: float = 0.01) -> bool:
        """Check if link is hot (in physics) vs cold (excluded).

        v1.2: hot if energy × weight > COLD_THRESHOLD
        """
        return self.heat_score > threshold

    def is_energy_carrier(self) -> bool:
        """Check if this link type carries energy.

        v1.2: expresses, about, attached_to, relates carry energy.
        """
        return self.type in [
            LinkType.EXPRESSES,
            LinkType.ABOUT,
            LinkType.ATTACHED_TO,
            LinkType.RELATES,
        ]


# =============================================================================
# EMOTION UTILITIES (v1.2)
# =============================================================================

def consolidate_emotions(emotions: List[List]) -> List[List]:
    """
    Merge duplicate emotions with diminishing returns.

    Example:
        [["fear", 0.7], ["respect", 0.4], ["fear", 0.3]]
        → [["fear", 0.85], ["respect", 0.4]]

    Uses diminishing returns: new = old + delta * (1 - old)
    So emotions asymptote toward 1.0 rather than hard clamping.
    """
    merged = {}
    for item in emotions:
        if len(item) != 2:
            continue
        emotion, intensity = item[0], float(item[1])
        if emotion in merged:
            # Diminishing returns
            merged[emotion] = min(1.0, merged[emotion] + intensity * (1 - merged[emotion]))
        else:
            merged[emotion] = min(1.0, max(0.0, intensity))
    return [[e, round(i, 3)] for e, i in merged.items()]


def add_emotion(
    emotions: List[List],
    emotion: str,
    intensity: float,
    max_emotions: int = 7
) -> List[List]:
    """
    Add an emotion to a list, consolidating duplicates.

    If max_emotions exceeded, drops lowest intensity emotions.

    Args:
        emotions: Current emotion list
        emotion: Emotion name to add
        intensity: Intensity [0, 1]
        max_emotions: Cap on list length (default 7)

    Returns:
        Updated emotion list
    """
    updated = emotions + [[emotion, intensity]]
    consolidated = consolidate_emotions(updated)

    # Cap at max_emotions, keeping highest intensity
    if len(consolidated) > max_emotions:
        consolidated.sort(key=lambda x: x[1], reverse=True)
        consolidated = consolidated[:max_emotions]

    return consolidated


def blend_emotions(
    link_emotions: List[List],
    incoming_emotions: List[List],
    blend_rate: float,
    max_emotions: int = 7
) -> List[List]:
    """
    Hebbian coloring: blend incoming emotions into link emotions.

    Energy flow colors the link — links "learn" what passes through them.

    Args:
        link_emotions: Current emotions on the link
        incoming_emotions: Emotions from the flowing moment
        blend_rate: How much to blend (typically flow/(flow+1))
        max_emotions: Cap on list length (default 7)

    Returns:
        Updated emotion list

    Example:
        link_emotions = [["trust", 0.5]]
        incoming_emotions = [["fear", 0.9], ["urgency", 0.6]]
        blend_rate = 0.3

        Result: [["trust", 0.5], ["fear", 0.27], ["urgency", 0.18]]
    """
    result = {e[0]: e[1] for e in link_emotions}

    for item in incoming_emotions:
        if len(item) != 2:
            continue
        name, intensity = item[0], float(item[1])
        incoming_contrib = intensity * blend_rate

        if name in result:
            # Diminishing returns
            result[name] = min(1.0, result[name] + incoming_contrib * (1 - result[name]))
        else:
            result[name] = min(1.0, incoming_contrib)

    # Convert back to list and cap
    emotion_list = [[e, round(i, 3)] for e, i in result.items() if i > 0.01]
    if len(emotion_list) > max_emotions:
        emotion_list.sort(key=lambda x: x[1], reverse=True)
        emotion_list = emotion_list[:max_emotions]

    return emotion_list


class ActorNarrative(BaseModel):
    """
    ACTOR_NARRATIVE - What an actor knows, believes, doubts, hides, or spreads.

    This link IS how actors know things. There is no "knowledge" stat.
    Aldric knows about the betrayal because he has a link to that narrative
    with heard=1.0 and believes=0.9.

    History: Every memory is mediated through a BELIEVES link. Actors can be
    wrong, confidence varies, sources can be traced.
    """
    # Link endpoints
    actor_id: str
    narrative_id: str

    # Knowledge (0-1) - how much do they know/believe?
    heard: float = Field(default=0.0, ge=0.0, le=1.0, description="Has encountered this story")
    believes: float = Field(default=0.0, ge=0.0, le=1.0, description="Holds as true")
    doubts: float = Field(default=0.0, ge=0.0, le=1.0, description="Actively uncertain")
    denies: float = Field(default=0.0, ge=0.0, le=1.0, description="Rejects as false")

    # Action (0-1) - what are they doing with this knowledge?
    hides: float = Field(default=0.0, ge=0.0, le=1.0, description="Knows but conceals")
    spreads: float = Field(default=0.0, ge=0.0, le=1.0, description="Actively promoting")

    # Origin
    originated: float = Field(default=0.0, ge=0.0, le=1.0, description="Created this narrative")

    # Metadata - how did they learn?
    source: BeliefSource = BeliefSource.NONE
    from_whom: str = Field(default="", description="Who told them")
    when: Optional[datetime] = None
    where: Optional[str] = Field(default=None, description="Place ID where they learned this")

    # Physics (v1.1: conductivity replaces weight/strength/energy)
    conductivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Percentage of energy that passes through")


class NarrativeNarrative(BaseModel):
    """
    NARRATIVE_NARRATIVE - How stories relate: contradict, support, elaborate, subsume, supersede.

    These links create story structure. Contradicting narratives create drama.
    Supporting narratives create belief clusters. Superseding narratives
    let the world evolve.
    """
    # Link endpoints
    source_narrative_id: str
    target_narrative_id: str

    # Relationship strengths (0-1)
    contradicts: float = Field(default=0.0, ge=0.0, le=1.0, description="Cannot both be true")
    supports: float = Field(default=0.0, ge=0.0, le=1.0, description="Reinforce each other")
    elaborates: float = Field(default=0.0, ge=0.0, le=1.0, description="Adds detail")
    subsumes: float = Field(default=0.0, ge=0.0, le=1.0, description="Specific case of")
    supersedes: float = Field(default=0.0, ge=0.0, le=1.0, description="Replaces - old fades")

    # Physics (v1.1: conductivity replaces weight/strength/energy)
    conductivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Percentage of energy that passes through")


class ActorSpace(BaseModel):
    """
    ACTOR_SPACE - Where an actor physically is (ground truth).

    This is GROUND TRUTH, not belief. An actor IS at a space,
    regardless of what anyone believes.
    """
    # Link endpoints
    actor_id: str
    space_id: str

    # Physical state
    present: float = Field(default=0.0, ge=0.0, le=1.0, description="1=here, 0=not here")
    visible: float = Field(default=1.0, ge=0.0, le=1.0, description="0=hiding, 1=visible")

    # Physics (v1.1: conductivity replaces weight/strength/energy)
    conductivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Percentage of energy that passes through")


class ActorThing(BaseModel):
    """
    ACTOR_THING - What an actor physically carries (ground truth).

    Ground truth. They HAVE it or they don't.
    Separate from ownership narratives (who SHOULD have it).
    """
    # Link endpoints
    actor_id: str
    thing_id: str

    # Physical state
    carries: float = Field(default=0.0, ge=0.0, le=1.0, description="1=has it, 0=doesn't")
    carries_hidden: float = Field(default=0.0, ge=0.0, le=1.0, description="1=secretly, 0=openly")

    # Physics (v1.1: conductivity replaces weight/strength/energy)
    conductivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Percentage of energy that passes through")


class ThingSpace(BaseModel):
    """
    THING_SPACE - Where an uncarried thing physically is (ground truth).

    Where things ARE, not where people think they are.
    """
    # Link endpoints
    thing_id: str
    space_id: str

    # Physical state
    located: float = Field(default=0.0, ge=0.0, le=1.0, description="1=here, 0=not here")
    hidden: float = Field(default=0.0, ge=0.0, le=1.0, description="1=concealed, 0=visible")
    specific_location: str = Field(default="", description="Where exactly")

    # Physics (v1.1: conductivity replaces weight/strength/energy)
    conductivity: float = Field(default=0.5, ge=0.0, le=1.0, description="Percentage of energy that passes through")


class SpaceSpace(BaseModel):
    """
    SPACE_SPACE - How locations connect: contains, path, borders (ground truth).

    Geography determines travel time, which affects proximity,
    which affects how much actors matter to the player.
    """
    # Link endpoints
    source_space_id: str
    target_space_id: str

    # Spatial relationships
    contains: float = Field(default=0.0, ge=0.0, le=1.0, description="This space is inside that")
    path: float = Field(default=0.0, ge=0.0, le=1.0, description="Can travel between")
    path_distance: str = Field(default="", description="How far: '2 days', '4 hours'")
    path_difficulty: PathDifficulty = PathDifficulty.MODERATE
    borders: float = Field(default=0.0, ge=0.0, le=1.0, description="Share a border")

    def travel_days(self) -> float:
        """Parse path_distance into days for proximity calculation."""
        if not self.path_distance:
            return 1.0

        dist = self.path_distance.lower()
        if 'adjacent' in dist or 'same' in dist:
            return 0.0
        elif 'hour' in dist:
            # Extract number of hours
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1)) / 24.0
            return 0.1
        elif 'day' in dist:
            import re
            match = re.search(r'(\d+)', dist)
            if match:
                return float(match.group(1))
            return 1.0
        else:
            return 1.0

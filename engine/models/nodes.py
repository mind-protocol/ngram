"""
Node Models — Generic Schema Types

The 5 node types: Actor, Space, Thing, Narrative, Moment
Based on schema.yaml v1.2

v1.2 CHANGES:
    - No decay — energy flows through links, cooling handles lifecycle
    - Moment.duration_minutes: affects radiation rate (1/duration×12 per tick)
    - Moments exit physics when all links cold (no LINGERING status)

v1.1 CHANGES:
    - MomentStatus: POSSIBLE, ACTIVE, COMPLETED, REJECTED, INTERRUPTED, OVERRIDDEN
    - Moment: tick_created, tick_activated, tick_resolved; prose/sketch fields
    - All nodes: energy/weight unbounded (no le=1.0)

DOCS: docs/schema/

TESTS:
    engine/tests/test_models.py::TestActorModel
    engine/tests/test_models.py::TestSpaceModel
    engine/tests/test_models.py::TestThingModel
    engine/tests/test_models.py::TestNarrativeModel
    engine/tests/test_models.py::TestMomentModel
    engine/tests/test_integration_scenarios.py (structural tests)

VALIDATES:
    V2.1: Actor invariants (id, name, type, voice, personality)
    V2.2: Space invariants (id, name, type, atmosphere)
    V2.3: Thing invariants (id, name, type, significance, portable)
    V2.4: Narrative invariants (id, name, content, type, weight, focus, truth)
    V2.6: Moment invariants (id, text, type, tick)

SEE ALSO:
    docs/engine/VALIDATION_Complete_Spec.md
    docs/engine/TEST_Complete_Spec.md
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from .base import (
    ActorType, Face, ActorVoice, Personality, Backstory, Modifier,
    SpaceType, Atmosphere,
    ThingType, Significance,
    NarrativeType, NarrativeTone, NarrativeVoice, NarrativeAbout,
    NarrativeSource,
    MomentType, MomentStatus, MomentTrigger
)


class Actor(BaseModel):
    """
    ACTOR - A person who exists in the world, with voice, history, and agency.
    Anyone who can act, speak, remember, die.
    """
    id: str
    name: str
    type: ActorType = ActorType.MINOR
    alive: bool = True
    face: Optional[Face] = None

    voice: ActorVoice = Field(default_factory=ActorVoice)
    personality: Personality = Field(default_factory=Personality)
    backstory: Backstory = Field(default_factory=Backstory)

    modifiers: List[Modifier] = Field(default_factory=list)

    # Physics metrics (v1.1: unbounded, no capacity — decay handles runaway)
    energy: float = Field(default=0.0, ge=0.0, description="Current energy level (unbounded)")
    weight: float = Field(default=1.0, ge=0.0, description="Importance/inertia (unbounded)")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.backstory.why_here:
            parts.append(f"Why here: {self.backstory.why_here}")
        if self.backstory.wound:
            parts.append(f"Wound: {self.backstory.wound}")
        if self.personality.values:
            parts.append(f"Values: {', '.join(v.value for v in self.personality.values)}")
        return ". ".join(parts)


class Space(BaseModel):
    """
    SPACE - A location where things happen, with atmosphere and geography.
    Anywhere that can be located, traveled to, occupied.
    """
    id: str
    name: str
    type: SpaceType = SpaceType.VILLAGE

    atmosphere: Atmosphere = Field(default_factory=Atmosphere)
    modifiers: List[Modifier] = Field(default_factory=list)

    # Physics metrics (v1.1: unbounded, no capacity — decay handles runaway)
    energy: float = Field(default=0.0, ge=0.0, description="Current energy level (unbounded)")
    weight: float = Field(default=1.0, ge=0.0, description="Importance/inertia (unbounded)")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.atmosphere.mood:
            parts.append(f"Mood: {self.atmosphere.mood.value}")
        if self.atmosphere.details:
            parts.append(f"Details: {', '.join(self.atmosphere.details)}")
        return ". ".join(parts)


class Thing(BaseModel):
    """
    THING - An object that can be owned, given, stolen, or fought over.
    Anything that can be possessed, transferred, contested.
    """
    id: str
    name: str
    type: ThingType = ThingType.TOOL
    portable: bool = True
    significance: Significance = Significance.MUNDANE
    quantity: int = 1
    description: str = ""

    modifiers: List[Modifier] = Field(default_factory=list)

    # Physics metrics (v1.1: unbounded, no capacity — decay handles runaway)
    energy: float = Field(default=0.0, ge=0.0, description="Current energy level (unbounded)")
    weight: float = Field(default=1.0, ge=0.0, description="Importance/inertia (unbounded)")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}, {self.type.value}"]
        if self.description:
            parts.append(self.description)
        if self.significance != Significance.MUNDANE:
            parts.append(f"Significance: {self.significance.value}")
        return ". ".join(parts)


class Narrative(BaseModel):
    """
    NARRATIVE - A story that characters believe, creating all relationships and knowledge.

    Core insight: Everything is story. "Aldric is loyal" is a narrative, not a stat.
    Characters believe narratives. They don't have relationships - they have stories
    they tell themselves about relationships.

    History insight: History is distributed. Narratives about the past exist as beliefs,
    not as a central event log. Player-experienced history points to conversation files;
    world-generated history carries its own detail.
    """
    id: str
    name: str
    content: str = Field(description="The story itself - what happened, what is believed")
    interpretation: str = Field(default="", description="What it means - emotional/thematic weight")

    type: NarrativeType

    about: NarrativeAbout = Field(default_factory=NarrativeAbout)
    tone: Optional[NarrativeTone] = None
    voice: NarrativeVoice = Field(default_factory=NarrativeVoice)

    # History fields - when did this happen?
    # NOTE: "where" is expressed via OCCURRED_AT link to Place, not an attribute
    occurred_at: Optional[str] = Field(default=None, description="When event happened: 'Day N, time_of_day'")

    # History content - ONE of these for historical narratives
    source: Optional[NarrativeSource] = Field(
        default=None,
        description="For player-experienced history: reference to conversation file section"
    )
    detail: Optional[str] = Field(
        default=None,
        description="For world-generated history: full description (no conversation exists)"
    )

    # Physics metrics (v1.1: unbounded, no capacity — decay handles runaway)
    energy: float = Field(default=0.0, ge=0.0, description="Current energy level (unbounded)")
    weight: float = Field(default=1.0, ge=0.0, description="Importance/inertia (unbounded)")
    focus: float = Field(default=1.0, ge=0.1, le=3.0, description="Narrator pacing adjustment")

    # Director only (hidden from players/characters)
    truth: float = Field(default=1.0, ge=0.0, le=1.0, description="How true is this? Characters never see this.")
    narrator_notes: str = Field(default="", description="Narrator's notes for continuity")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    def embeddable_text(self) -> str:
        """Generate text for embedding."""
        parts = [f"{self.name}: {self.content}"]
        if self.interpretation:
            parts.append(f"Meaning: {self.interpretation}")
        if self.tone:
            parts.append(f"Tone: {self.tone.value}")
        return ". ".join(parts)

    @property
    def is_core_type(self) -> bool:
        """Core types (oath, blood, debt) decay slower."""
        return self.type in [NarrativeType.OATH, NarrativeType.BLOOD, NarrativeType.DEBT]


class Moment(BaseModel):
    """
    MOMENT - A single unit of narrated content OR a potential moment.

    In the Moment Graph architecture, moments exist in a possibility space.
    They can be:
    - possible: Created but not yet surfaced
    - active: Visible to player, can be triggered
    - spoken: Part of history
    - dormant: Waiting for player return
    - decayed: Pruned

    Links:
        Actor -[CAN_SPEAK]-> Moment (who can say this)
        Actor -[SAID]-> Moment (who said this - after spoken)
        Moment -[ATTACHED_TO]-> Actor|Space|Thing|Narrative
        Moment -[CAN_LEAD_TO]-> Moment (traversal)
        Moment -[THEN]-> Moment (sequence after spoken)
        Moment -[AT]-> Space (where it occurred)
        Narrative -[FROM]-> Moment (source attribution)

    Note: Speaker is NOT an attribute - use SAID link to find who spoke.
    """
    id: str = Field(description="Unique ID: {place}_{day}_{time}_{type}_{timestamp}")
    type: MomentType = MomentType.NARRATION

    # Content (v1.1: prose written at creation, shown at completion)
    prose: str = Field(
        default="",
        description="Full prose text — written at creation, shown at completion"
    )
    sketch: Optional[str] = Field(
        default=None,
        description="Brief description for world builder moments (optional)"
    )

    # Legacy field (deprecated, use prose instead)
    text: str = Field(default="", description="DEPRECATED: use prose instead")

    # Moment Graph fields (v1.2)
    status: MomentStatus = Field(
        default=MomentStatus.POSSIBLE,
        description="Lifecycle status in moment graph"
    )
    energy: float = Field(
        default=0.0,
        ge=0.0,
        description="Current energy level (unbounded, no decay — depletes via radiation)"
    )
    weight: float = Field(
        default=0.5,
        ge=0.0,
        description="Salience/importance (unbounded)"
    )
    duration_minutes: float = Field(
        default=0.5,
        ge=0.0,
        description="Expected duration — affects radiation rate (1/duration×12 per tick)"
    )
    tone: Optional[str] = Field(
        default=None,
        description="Emotional tone: bitter, hopeful, urgent, etc."
    )

    # Tick tracking (v1.1)
    tick_created: int = Field(
        default=0, ge=0,
        description="World tick when moment was created"
    )
    tick_activated: Optional[int] = Field(
        default=None,
        description="World tick when moment became active (possible→active)"
    )
    tick_resolved: Optional[int] = Field(
        default=None,
        description="World tick when moment was resolved (completed/rejected/interrupted/overridden)"
    )

    # Transcript reference - line number in playthroughs/{id}/transcript.json
    line: Optional[int] = Field(default=None, description="Starting line in transcript.json")

    # Speaker reference (derived from SAID link, not stored on node)
    speaker: Optional[str] = Field(default=None, description="Actor ID for dialogue moments")

    # Embedding for semantic search
    embedding: Optional[List[float]] = Field(default=None, exclude=True)

    # Query fields (for backstory generation)
    query: Optional[str] = Field(
        default=None,
        description="Question this moment asks (triggers backstory generation)"
    )
    query_type: Optional[str] = Field(
        default=None,
        description="Type of query: backstory_gap, clarification, etc."
    )
    query_filled: bool = Field(
        default=False,
        description="Whether the query has been answered"
    )

    def embeddable_text(self) -> str:
        """Generate text for embedding (speaker added by processor if dialogue)."""
        content = self.prose or self.text  # prefer prose, fallback to text
        if self.type == MomentType.DIALOGUE and self.speaker:
            return f"{self.speaker}: {content}"
        return content

    @property
    def should_embed(self) -> bool:
        """Only embed if content is meaningful length."""
        content = self.prose or self.text
        return len(content.strip()) > 20

    @property
    def is_active(self) -> bool:
        """Check if moment is currently active (drawing/flowing energy)."""
        return self.status == MomentStatus.ACTIVE

    @property
    def is_completed(self) -> bool:
        """Check if moment has been completed (liquidated, now inert bridge)."""
        return self.status == MomentStatus.COMPLETED

    @property
    def is_resolved(self) -> bool:
        """Check if moment has reached a terminal state."""
        return self.status in [
            MomentStatus.COMPLETED,
            MomentStatus.REJECTED,
            MomentStatus.INTERRUPTED,
            MomentStatus.OVERRIDDEN
        ]

    @property
    def can_draw_energy(self) -> bool:
        """Check if moment can draw energy from connected actors.

        v1.2: Both POSSIBLE and ACTIVE moments draw (POSSIBLE at reduced rate).
        """
        return self.status in [MomentStatus.POSSIBLE, MomentStatus.ACTIVE]

    @property
    def radiation_rate(self) -> float:
        """Calculate radiation rate based on duration.

        v1.2: radiation_rate = 1 / (duration_minutes × 12)
        12 ticks per minute (5 sec tick).
        """
        if self.duration_minutes <= 0:
            return 1.0  # instant
        return 1.0 / (self.duration_minutes * 12)


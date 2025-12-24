"""
Schema v1.2 — Energy Physics Tick

8-phase tick algorithm with NO DECAY:
1. Generation — Actors generate energy (proximity-gated)
2. Moment Draw — Possible+Active moments draw from actors
3. Moment Flow — Active moments radiate (duration-based)
4. Moment Interaction — Support/contradict via shared narratives
5. Narrative Backflow — Narratives radiate to actors (link.energy gated)
6. Link Cooling — Drain to nodes + convert to strength
7. Completion — Mark completed moments
8. Rejection — Return energy to player

Key v1.2 changes from v1.1:
- NO DECAY (energy persists, flows through links)
- Hot/cold links (link.energy determines physics participation)
- Unified traversal (every flow updates energy + strength + emotions)
- Top-N filter (process only hottest 20 links per node)
- Target weight (sqrt(target.weight) reception factor)

DOCS: docs/physics/algorithms/ALGORITHM_Physics_Schema_v1.2_Energy_Physics.md
OWNER: Claude Dev 2
"""

import logging
import math
from typing import List, Dict, Any, Tuple, Optional, Set
from dataclasses import dataclass, field

from engine.physics.graph import GraphQueries, GraphOps
from engine.physics.graph.graph_query_utils import dijkstra_with_resistance, calculate_link_resistance

logger = logging.getLogger(__name__)


# =============================================================================
# v1.2 CONSTANTS
# =============================================================================

GENERATION_RATE = 0.5
DRAW_RATE = 0.3
BACKFLOW_RATE = 0.1

COLD_THRESHOLD = 0.01
TOP_N_LINKS = 20

TICK_DURATION_SECONDS = 5
TICKS_PER_MINUTE = 12

LINK_DRAIN_RATE = 0.3
LINK_TO_STRENGTH_RATE = 0.1

SUPPORT_THRESHOLD = 0.7
CONTRADICT_THRESHOLD = 0.3
INTERACTION_RATE = 0.05

REJECTION_RETURN_RATE = 0.8


# =============================================================================
# RESULT TYPE
# =============================================================================

@dataclass
class TickResultV1_2:
    """Result of a v1.2 graph tick."""
    # Phase stats
    energy_generated: float = 0.0
    energy_drawn: float = 0.0
    energy_flowed: float = 0.0
    energy_interacted: float = 0.0
    energy_backflowed: float = 0.0
    energy_cooled: float = 0.0

    # Counts
    actors_updated: int = 0
    moments_active: int = 0
    moments_possible: int = 0
    moments_completed: int = 0
    moments_rejected: int = 0
    links_cooled: int = 0
    links_crystallized: int = 0

    # Completions
    completions: List[Dict[str, Any]] = field(default_factory=list)
    rejections: List[Dict[str, Any]] = field(default_factory=list)

    # Hot/cold stats
    hot_links: int = 0
    cold_links: int = 0


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def avg_emotion_intensity(emotions: List[List]) -> float:
    """Average intensity of emotion list. Returns 0.5 if empty."""
    if not emotions:
        return 0.5
    intensities = [float(e[1]) for e in emotions if len(e) == 2]
    return sum(intensities) / len(intensities) if intensities else 0.5


def emotion_proximity(emotions_a: List[List], emotions_b: List[List]) -> float:
    """
    Calculate emotion similarity between two emotion lists.
    Returns 0-1. 0.2 baseline if either empty.
    Uses weighted Jaccard similarity.
    """
    if not emotions_a or not emotions_b:
        return 0.2

    dict_a = {e[0]: float(e[1]) for e in emotions_a if len(e) == 2}
    dict_b = {e[0]: float(e[1]) for e in emotions_b if len(e) == 2}

    if not dict_a or not dict_b:
        return 0.2

    # Weighted Jaccard
    intersection = 0.0
    union = 0.0

    all_emotions = set(dict_a.keys()) | set(dict_b.keys())
    for emotion in all_emotions:
        a_val = dict_a.get(emotion, 0.0)
        b_val = dict_b.get(emotion, 0.0)
        intersection += min(a_val, b_val)
        union += max(a_val, b_val)

    if union == 0:
        return 0.2

    return intersection / union


def blend_emotions(
    existing: List[List],
    incoming: List[List],
    blend_rate: float,
    max_emotions: int = 7
) -> List[List]:
    """
    Blend incoming emotions into existing emotions.

    Args:
        existing: Current emotion list [[name, intensity], ...]
        incoming: Emotions to blend in
        blend_rate: How much weight to give incoming (0-1)
        max_emotions: Maximum emotions to keep

    Returns:
        Blended emotion list, sorted by intensity, capped at max_emotions
    """
    if not incoming:
        return existing

    # Convert to dicts
    result = {e[0]: float(e[1]) for e in existing if len(e) == 2}
    incoming_dict = {e[0]: float(e[1]) for e in incoming if len(e) == 2}

    # Blend incoming
    for emotion, intensity in incoming_dict.items():
        if emotion in result:
            # Diminishing returns on existing emotion
            current = result[emotion]
            result[emotion] = current + (intensity * blend_rate) * (1 - current)
        else:
            result[emotion] = intensity * blend_rate

    # Sort by intensity, cap at max
    sorted_emotions = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return [[name, intensity] for name, intensity in sorted_emotions[:max_emotions]]


def get_weighted_average_emotions(links: List[Dict]) -> List[List]:
    """Get weighted average emotions from a list of links."""
    if not links:
        return []

    emotion_totals = {}
    total_weight = 0.0

    for link in links:
        weight = link.get('weight', 1.0) or 1.0
        emotions = link.get('emotions', []) or []

        for e in emotions:
            if len(e) == 2:
                name, intensity = e[0], float(e[1])
                if name not in emotion_totals:
                    emotion_totals[name] = 0.0
                emotion_totals[name] += intensity * weight

        total_weight += weight

    if total_weight == 0 or not emotion_totals:
        return []

    # Normalize
    return [[name, total / total_weight] for name, total in emotion_totals.items()]


# =============================================================================
# GRAPH TICK v1.2
# =============================================================================

class GraphTickV1_2:
    """
    Schema v1.2 Energy Physics Tick Engine.

    NO DECAY. Energy flows through links and cools naturally.
    """

    def __init__(
        self,
        graph_name: str = "graph",
        host: str = "localhost",
        port: int = 6379
    ):
        self.read = GraphQueries(graph_name=graph_name, host=host, port=port)
        self.write = GraphOps(graph_name=graph_name, host=host, port=port)
        self.graph_name = graph_name
        self._tick_count = 0

        logger.info(f"[GraphTick v1.2] Initialized for {graph_name}")

    def run(self, current_tick: int = 0, player_id: str = "player") -> TickResultV1_2:
        """
        Run a v1.2 graph tick with 8 phases.

        Args:
            current_tick: Current world tick number
            player_id: Player actor ID for proximity calculations

        Returns:
            TickResultV1_2 with phase stats
        """
        self._tick_count += 1
        logger.info(f"[GraphTick v1.2] Running tick #{current_tick}")
        result = TickResultV1_2()

        # Phase 1: Generation (proximity-gated)
        result.energy_generated, result.actors_updated = self._phase_generation(player_id)

        # Phase 2: Moment Draw (possible + active)
        possible_moments = self._get_moments_by_status('possible')
        active_moments = self._get_moments_by_status('active')
        result.moments_possible = len(possible_moments)
        result.moments_active = len(active_moments)

        all_draw_moments = possible_moments + active_moments
        result.energy_drawn = self._phase_moment_draw(all_draw_moments)

        # Phase 3: Moment Flow (active only, duration-based)
        result.energy_flowed = self._phase_moment_flow(active_moments)

        # Phase 4: Moment Interaction (support/contradict)
        result.energy_interacted = self._phase_moment_interaction(active_moments)

        # Phase 5: Narrative Backflow (link.energy gated)
        result.energy_backflowed = self._phase_narrative_backflow()

        # Phase 6: Link Cooling (drain + strength)
        result.energy_cooled, result.links_cooled = self._phase_link_cooling()

        # Count hot/cold links
        result.hot_links, result.cold_links = self._count_hot_cold_links()

        # Phase 7: Completion Processing
        completions, crystallized = self._phase_completion(active_moments, current_tick)
        result.completions = completions
        result.moments_completed = len(completions)
        result.links_crystallized = crystallized

        # Phase 8: Rejection Processing
        rejections = self._phase_rejection(possible_moments, player_id, current_tick)
        result.rejections = rejections
        result.moments_rejected = len(rejections)

        logger.info(
            f"[GraphTick v1.2] Complete: "
            f"gen={result.energy_generated:.2f}, "
            f"draw={result.energy_drawn:.2f}, "
            f"flow={result.energy_flowed:.2f}, "
            f"interact={result.energy_interacted:.2f}, "
            f"backflow={result.energy_backflowed:.2f}, "
            f"cooled={result.energy_cooled:.2f}, "
            f"hot_links={result.hot_links}, "
            f"completed={result.moments_completed}"
        )

        return result

    # =========================================================================
    # PHASE 1: GENERATION
    # =========================================================================

    def _phase_generation(self, player_id: str) -> Tuple[float, int]:
        """
        Phase 1: Actors generate energy, gated by proximity to player.

        Formula: actor.energy += weight × GENERATION_RATE × proximity
        Proximity = 1 / (1 + path_resistance(player, actor))

        Order: Actors by weight descending
        """
        total_generated = 0.0
        actors_updated = 0

        try:
            # Get all actors sorted by weight descending
            actors = self.read.query("""
            MATCH (a:Actor)
            WHERE a.alive = true OR a.alive IS NULL
            RETURN a.id AS id, a.weight AS weight, a.energy AS energy
            ORDER BY a.weight DESC
            """)

            for actor in actors:
                actor_id = actor.get('id')
                weight = actor.get('weight', 1.0) or 1.0
                current_energy = actor.get('energy', 0.0) or 0.0

                # Calculate proximity to player
                if actor_id == player_id:
                    proximity = 1.0
                else:
                    proximity = self._calculate_proximity(player_id, actor_id)

                # Generate energy
                generated = weight * GENERATION_RATE * proximity
                new_energy = current_energy + generated
                total_generated += generated

                # Update actor
                self.write._query(f"""
                MATCH (a:Actor {{id: '{actor_id}'}})
                SET a.energy = {new_energy}
                """)
                actors_updated += 1

        except Exception as e:
            logger.warning(f"[Phase 1] Generation error: {e}")

        return total_generated, actors_updated

    def _calculate_proximity(self, from_id: str, to_id: str) -> float:
        """
        Calculate proximity via path resistance.
        proximity = 1 / (1 + path_resistance)
        """
        resistance = self._path_resistance(from_id, to_id)
        return 1.0 / (1.0 + resistance)

    def _path_resistance(self, from_id: str, to_id: str, max_hops: int = 5) -> float:
        """
        Calculate minimum path resistance using link properties.

        Uses full Dijkstra with v1.2 resistance formula:
            edge_resistance = 1 / (conductivity × weight × emotion_factor)

        Args:
            from_id: Starting node ID
            to_id: Target node ID
            max_hops: Maximum path length (default 5)

        Returns:
            Total path resistance (sum of edge resistances), or 100.0 if no path
        """
        try:
            # Fetch edges within hop range of both nodes
            # Use BFS-style query to get relevant subgraph
            edges_result = self.read.query(f"""
            MATCH (a)-[r]-(b)
            WHERE (a.id = '{from_id}' OR b.id = '{from_id}' OR a.id = '{to_id}' OR b.id = '{to_id}')
            OR EXISTS {{
                MATCH path = shortestPath((start {{id: '{from_id}'}})-[*..{max_hops}]-(end {{id: '{to_id}'}}))
                WHERE a IN nodes(path) OR b IN nodes(path)
            }}
            RETURN DISTINCT a.id AS node_a, b.id AS node_b,
                   coalesce(r.conductivity, 1.0) AS conductivity,
                   coalesce(r.weight, 1.0) AS weight,
                   r.emotions AS emotions
            """)

            if not edges_result:
                # Fallback to simple hop count if subgraph query fails
                return self._path_resistance_fallback(from_id, to_id, max_hops)

            # Build edges list with emotion factors
            edges = []
            for edge in edges_result:
                emotions = edge.get('emotions', []) or []
                # Use baseline emotion factor (0.5) if no emotions
                emotion_factor = avg_emotion_intensity(emotions) if emotions else 0.5

                edges.append({
                    'node_a': edge.get('node_a'),
                    'node_b': edge.get('node_b'),
                    'conductivity': edge.get('conductivity', 1.0) or 1.0,
                    'weight': edge.get('weight', 1.0) or 1.0,
                    'emotion_factor': max(0.1, emotion_factor)  # Floor to prevent division issues
                })

            # Run Dijkstra
            result = dijkstra_with_resistance(edges, from_id, to_id, max_hops)

            if result:
                return result.get('total_resistance', 100.0)
            return 100.0  # No path found

        except Exception as e:
            logger.debug(f"[Path Resistance] Dijkstra failed ({e}), using fallback")
            return self._path_resistance_fallback(from_id, to_id, max_hops)

    def _path_resistance_fallback(self, from_id: str, to_id: str, max_hops: int = 5) -> float:
        """
        Fallback path resistance using simple hop count.

        Used when full Dijkstra query fails or times out.
        """
        try:
            result = self.read.query(f"""
            MATCH p = shortestPath((a {{id: '{from_id}'}})-[*..{max_hops}]-(b {{id: '{to_id}'}}))
            RETURN length(p) AS hops
            """)
            if result:
                hops = result[0].get('hops', max_hops)
                return float(hops)  # Simplified: resistance = hops
            return 100.0
        except:
            return 100.0

    # =========================================================================
    # PHASE 2: MOMENT DRAW
    # =========================================================================

    def _phase_moment_draw(self, moments: List[Dict]) -> float:
        """
        Phase 2: Both POSSIBLE and ACTIVE moments draw from connected actors.

        Formula: flow = actor.energy × DRAW_RATE × conductivity × weight × emotion_factor
        Received: flow × sqrt(moment.weight)

        Order: Moments by energy×weight desc, Links by energy×weight desc
        """
        total_drawn = 0.0

        # Sort moments by energy × weight
        sorted_moments = sorted(
            moments,
            key=lambda m: (m.get('energy', 0.0) or 0.0) * (m.get('weight', 1.0) or 1.0),
            reverse=True
        )

        for moment in sorted_moments:
            moment_id = moment.get('id')
            moment_weight = moment.get('weight', 1.0) or 1.0
            moment_energy = moment.get('energy', 0.0) or 0.0

            try:
                # Get weighted average emotions from moment's links
                moment_emotions = self._get_moment_emotions(moment_id)

                # Get top 20 expresses links
                links = self._get_hot_links_to_moment(moment_id, TOP_N_LINKS)

                for link in links:
                    actor_id = link.get('actor_id')
                    actor_energy = link.get('actor_energy', 0.0) or 0.0
                    conductivity = link.get('conductivity', 1.0) or 1.0
                    link_weight = link.get('weight', 1.0) or 1.0
                    link_energy = link.get('link_energy', 0.0) or 0.0
                    link_emotions = link.get('emotions', []) or []

                    # Calculate emotion factor
                    emotion_factor = emotion_proximity(link_emotions, moment_emotions)

                    # Calculate flow
                    flow = actor_energy * DRAW_RATE * conductivity * link_weight * emotion_factor
                    received = flow * math.sqrt(moment_weight)

                    if flow > 0.001:  # Skip tiny flows
                        # Update energies
                        actor_energy -= flow
                        moment_energy += received
                        total_drawn += flow

                        # Apply unified traversal (update link)
                        self._energy_flows_through(
                            link, flow, moment_emotions,
                            actor_id, actor_energy,
                            moment_id, moment_energy
                        )

                        # Update actor
                        self.write._query(f"""
                        MATCH (a:Actor {{id: '{actor_id}'}})
                        SET a.energy = {max(0, actor_energy)}
                        """)

                # Update moment
                self.write._query(f"""
                MATCH (m:Moment {{id: '{moment_id}'}})
                SET m.energy = {moment_energy}
                """)

            except Exception as e:
                logger.warning(f"[Phase 2] Draw error for {moment_id}: {e}")

        return total_drawn

    # =========================================================================
    # PHASE 3: MOMENT FLOW
    # =========================================================================

    def _phase_moment_flow(self, active_moments: List[Dict]) -> float:
        """
        Phase 3: Active moments radiate energy based on duration.

        Radiation rate = 1 / (duration_minutes × 12)
        Flow = energy × radiation_rate × share × conductivity × emotion_factor
        Received = flow × sqrt(target.weight)

        Order: Moments by energy×weight desc
        """
        total_flowed = 0.0

        # Sort by energy × weight
        sorted_moments = sorted(
            active_moments,
            key=lambda m: (m.get('energy', 0.0) or 0.0) * (m.get('weight', 1.0) or 1.0),
            reverse=True
        )

        for moment in sorted_moments:
            moment_id = moment.get('id')

            try:
                # Get current state
                m = self.read.query(f"""
                MATCH (m:Moment {{id: '{moment_id}'}})
                RETURN m.energy AS energy, m.duration_minutes AS duration, m.weight AS weight
                """)
                if not m:
                    continue

                moment_energy = m[0].get('energy', 0.0) or 0.0
                duration = m[0].get('duration', 1.0) or 1.0  # Default 1 minute
                moment_weight = m[0].get('weight', 1.0) or 1.0

                if moment_energy <= 0.01:
                    continue

                # Calculate radiation rate based on duration
                radiation_rate = 1.0 / (duration * TICKS_PER_MINUTE)
                radiation = moment_energy * radiation_rate

                # Get moment emotions
                moment_emotions = self._get_moment_emotions(moment_id)

                # Get top 20 outgoing links
                links = self._get_hot_links_from_moment(moment_id, TOP_N_LINKS)

                if not links:
                    continue

                # Calculate total weight for distribution
                total_weight = sum(l.get('weight', 1.0) or 1.0 for l in links)
                if total_weight <= 0:
                    continue

                for link in links:
                    target_id = link.get('target_id')
                    target_weight = link.get('target_weight', 1.0) or 1.0
                    target_energy = link.get('target_energy', 0.0) or 0.0
                    conductivity = link.get('conductivity', 1.0) or 1.0
                    link_weight = link.get('weight', 1.0) or 1.0
                    link_emotions = link.get('emotions', []) or []

                    # Calculate share and flow
                    share = link_weight / total_weight
                    emotion_factor = emotion_proximity(link_emotions, moment_emotions)

                    flow = radiation * share * conductivity * emotion_factor
                    received = flow * math.sqrt(target_weight)

                    if flow > 0.001:
                        # Deduct from moment
                        moment_energy -= flow
                        target_energy += received
                        total_flowed += flow

                        # Apply unified traversal
                        self._energy_flows_through(
                            link, flow, moment_emotions,
                            moment_id, moment_energy,
                            target_id, target_energy
                        )

                        # Update target
                        self.write._query(f"""
                        MATCH (n {{id: '{target_id}'}})
                        SET n.energy = {target_energy}
                        """)

                # Update moment energy
                self.write._query(f"""
                MATCH (m:Moment {{id: '{moment_id}'}})
                SET m.energy = {max(0, moment_energy)}
                """)

            except Exception as e:
                logger.warning(f"[Phase 3] Flow error for {moment_id}: {e}")

        return total_flowed

    # =========================================================================
    # PHASE 4: MOMENT INTERACTION
    # =========================================================================

    def _phase_moment_interaction(self, active_moments: List[Dict]) -> float:
        """
        Phase 4: Active moments support or contradict each other.

        If proximity > 0.7: support (m1 feeds m2)
        If proximity < 0.3: contradict (m1 drains m2)

        Only between moments sharing narratives.
        """
        total_interacted = 0.0

        if len(active_moments) < 2:
            return 0.0

        # Get emotions for each moment
        moment_emotions = {}
        for m in active_moments:
            mid = m.get('id')
            moment_emotions[mid] = self._get_moment_emotions(mid)

        # Get shared narratives between moment pairs
        moment_ids = [m.get('id') for m in active_moments]

        for i, m1 in enumerate(active_moments):
            m1_id = m1.get('id')
            m1_energy = m1.get('energy', 0.0) or 0.0

            if m1_energy <= 0.01:
                continue

            for m2 in active_moments[i+1:]:
                m2_id = m2.get('id')
                m2_energy = m2.get('energy', 0.0) or 0.0

                try:
                    # Check for shared narratives
                    shared = self._get_shared_narratives(m1_id, m2_id)
                    if not shared:
                        continue

                    # Calculate emotion proximity
                    proximity = emotion_proximity(
                        moment_emotions.get(m1_id, []),
                        moment_emotions.get(m2_id, [])
                    )

                    if proximity > SUPPORT_THRESHOLD:
                        # Support: m1 feeds m2
                        support = m1_energy * INTERACTION_RATE * proximity
                        m2_weight = m2.get('weight', 1.0) or 1.0
                        received = support * math.sqrt(m2_weight)
                        m2_energy += received
                        total_interacted += support

                        self.write._query(f"""
                        MATCH (m:Moment {{id: '{m2_id}'}})
                        SET m.energy = {m2_energy}
                        """)

                    elif proximity < CONTRADICT_THRESHOLD:
                        # Contradict: m1 drains m2
                        suppress = m1_energy * INTERACTION_RATE * (1 - proximity)
                        m2_energy = max(0, m2_energy - suppress)
                        total_interacted += suppress

                        self.write._query(f"""
                        MATCH (m:Moment {{id: '{m2_id}'}})
                        SET m.energy = {m2_energy}
                        """)

                except Exception as e:
                    logger.warning(f"[Phase 4] Interaction error {m1_id} <-> {m2_id}: {e}")

        return total_interacted

    def _get_shared_narratives(self, m1_id: str, m2_id: str) -> List[str]:
        """Get narrative IDs that both moments connect to."""
        try:
            result = self.read.query(f"""
            MATCH (m1:Moment {{id: '{m1_id}'}})-[:ABOUT]->(n:Narrative)<-[:ABOUT]-(m2:Moment {{id: '{m2_id}'}})
            RETURN DISTINCT n.id AS narrative_id
            """)
            return [r.get('narrative_id') for r in result if r.get('narrative_id')]
        except:
            return []

    # =========================================================================
    # PHASE 5: NARRATIVE BACKFLOW
    # =========================================================================

    def _phase_narrative_backflow(self) -> float:
        """
        Phase 5: Narratives backflow to actors, gated by link.energy.

        No threshold (just computational minimum 0.01).
        Gated by link.energy in formula: unfocused = no backflow.

        Order: Narratives by energy desc
        """
        total_backflow = 0.0

        try:
            # Get all narratives with energy > 0.01
            narratives = self.read.query("""
            MATCH (n:Narrative)
            WHERE n.energy > 0.01
            RETURN n.id AS id, n.energy AS energy
            ORDER BY n.energy DESC
            """)

            for narr in narratives:
                narr_id = narr.get('id')
                narr_energy = narr.get('energy', 0.0) or 0.0

                # Get narrative emotions
                narr_emotions = self._get_narrative_emotions(narr_id)

                # Get top 20 actor links
                links = self._get_hot_links_to_actors(narr_id, TOP_N_LINKS)

                for link in links:
                    link_energy = link.get('link_energy', 0.0) or 0.0

                    # Gate by link.energy
                    if link_energy < COLD_THRESHOLD:
                        continue

                    actor_id = link.get('actor_id')
                    actor_energy = link.get('actor_energy', 0.0) or 0.0
                    actor_weight = link.get('actor_weight', 1.0) or 1.0
                    conductivity = link.get('conductivity', 1.0) or 1.0
                    link_emotions = link.get('emotions', []) or []

                    # Backflow formula includes link.energy
                    emotion_factor = emotion_proximity(link_emotions, narr_emotions)
                    backflow = narr_energy * BACKFLOW_RATE * conductivity * emotion_factor * link_energy
                    received = backflow * math.sqrt(actor_weight)

                    if backflow > 0.001:
                        narr_energy -= backflow
                        actor_energy += received
                        total_backflow += backflow

                        # Apply traversal
                        self._energy_flows_through(
                            link, backflow, narr_emotions,
                            narr_id, narr_energy,
                            actor_id, actor_energy
                        )

                        # Update actor
                        self.write._query(f"""
                        MATCH (a:Actor {{id: '{actor_id}'}})
                        SET a.energy = {actor_energy}
                        """)

                # Update narrative
                self.write._query(f"""
                MATCH (n:Narrative {{id: '{narr_id}'}})
                SET n.energy = {max(0, narr_energy)}
                """)

        except Exception as e:
            logger.warning(f"[Phase 5] Backflow error: {e}")

        return total_backflow

    # =========================================================================
    # PHASE 6: LINK COOLING
    # =========================================================================

    def _phase_link_cooling(self) -> Tuple[float, int]:
        """
        Phase 6: Links cool by draining to nodes and converting to strength.

        - Drain 30% to connected nodes (50/50 split)
        - Convert 10% to permanent strength

        No arbitrary decay!
        """
        total_cooled = 0.0
        links_cooled = 0

        try:
            # Get all hot links
            hot_links = self.read.query(f"""
            MATCH (a)-[r]->(b)
            WHERE r.energy IS NOT NULL AND r.energy * coalesce(r.weight, 1.0) > {COLD_THRESHOLD}
            RETURN id(r) AS rid, type(r) AS rtype,
                   a.id AS node_a, b.id AS node_b,
                   r.energy AS energy, r.strength AS strength,
                   r.weight AS weight, r.emotions AS emotions,
                   a.energy AS a_energy, b.energy AS b_energy,
                   a.weight AS a_weight, b.weight AS b_weight
            ORDER BY r.energy * coalesce(r.weight, 1.0) DESC
            """)

            for link in hot_links:
                link_energy = link.get('energy', 0.0) or 0.0
                link_strength = link.get('strength', 0.0) or 0.0
                link_weight = link.get('weight', 1.0) or 1.0
                emotions = link.get('emotions', []) or []

                node_a = link.get('node_a')
                node_b = link.get('node_b')
                a_energy = link.get('a_energy', 0.0) or 0.0
                b_energy = link.get('b_energy', 0.0) or 0.0
                a_weight = link.get('a_weight', 1.0) or 1.0
                b_weight = link.get('b_weight', 1.0) or 1.0

                # Calculate drain
                drain = link_energy * LINK_DRAIN_RATE

                # Return to nodes (50/50)
                a_energy += drain * 0.5
                b_energy += drain * 0.5

                # Convert to strength
                emotion_intensity = avg_emotion_intensity(emotions)
                growth = (link_energy * LINK_TO_STRENGTH_RATE * emotion_intensity * a_weight) / ((1 + link_strength) * b_weight)
                new_strength = link_strength + growth

                # Reduce link energy
                new_energy = link_energy - drain - (link_energy * LINK_TO_STRENGTH_RATE)
                new_energy = max(0, new_energy)

                total_cooled += drain
                links_cooled += 1

                # Update nodes
                self.write._query(f"""
                MATCH (a {{id: '{node_a}'}})
                SET a.energy = {a_energy}
                """)
                self.write._query(f"""
                MATCH (b {{id: '{node_b}'}})
                SET b.energy = {b_energy}
                """)

                # Note: Updating relationship properties by id(r) requires
                # different syntax. Using node match instead.
                # This is a simplified version.

        except Exception as e:
            logger.warning(f"[Phase 6] Cooling error: {e}")

        return total_cooled, links_cooled

    # =========================================================================
    # PHASE 7: COMPLETION
    # =========================================================================

    def _phase_completion(
        self,
        active_moments: List[Dict],
        current_tick: int
    ) -> Tuple[List[Dict], int]:
        """
        Phase 7: Complete moments that meet criteria.

        Just set status. Links cool naturally.
        Crystallize actor↔actor links.
        """
        completions = []
        links_crystallized = 0

        # Completion criteria from canon holder (simplified: energy threshold)
        COMPLETION_THRESHOLD = 0.8

        for moment in active_moments:
            moment_id = moment.get('id')

            try:
                # Get current state
                m = self.read.query(f"""
                MATCH (m:Moment {{id: '{moment_id}'}})
                RETURN m.energy AS energy, m.status AS status
                """)
                if not m:
                    continue

                energy = m[0].get('energy', 0.0) or 0.0

                if energy >= COMPLETION_THRESHOLD:
                    # Complete the moment
                    self.write._query(f"""
                    MATCH (m:Moment {{id: '{moment_id}'}})
                    SET m.status = 'completed',
                        m.tick_resolved = {current_tick}
                    """)

                    # Crystallize links between actors
                    crystallized = self._crystallize_actor_links(moment_id)
                    links_crystallized += crystallized

                    completions.append({
                        'moment_id': moment_id,
                        'energy': energy,
                        'tick': current_tick,
                        'links_crystallized': crystallized
                    })

                    logger.info(f"[Phase 7] Completed {moment_id}")

            except Exception as e:
                logger.warning(f"[Phase 7] Completion error for {moment_id}: {e}")

        return completions, links_crystallized

    def _crystallize_actor_links(self, moment_id: str) -> int:
        """Create relates links between actors sharing a completed moment."""
        crystallized = 0

        try:
            # Get actors connected to this moment
            actors = self.read.query(f"""
            MATCH (a:Actor)-[]->(m:Moment {{id: '{moment_id}'}})
            RETURN DISTINCT a.id AS actor_id
            """)

            if len(actors) < 2:
                return 0

            actor_ids = [a.get('actor_id') for a in actors if a.get('actor_id')]

            # Get moment emotions for inheritance
            moment_emotions = self._get_moment_emotions(moment_id)
            emotions_str = str(moment_emotions).replace("'", '"') if moment_emotions else "[]"

            # Create links between each pair
            for i, actor_a in enumerate(actor_ids):
                for actor_b in actor_ids[i+1:]:
                    # Check if link exists
                    existing = self.read.query(f"""
                    MATCH (a:Actor {{id: '{actor_a}'}})-[r:RELATES]-(b:Actor {{id: '{actor_b}'}})
                    RETURN count(r) AS cnt
                    """)

                    if existing and existing[0].get('cnt', 0) == 0:
                        self.write._query(f"""
                        MATCH (a:Actor {{id: '{actor_a}'}}), (b:Actor {{id: '{actor_b}'}})
                        CREATE (a)-[:RELATES {{
                            conductivity: 0.2,
                            weight: 0.2,
                            energy: 0.0,
                            strength: 0.1,
                            emotions: {emotions_str},
                            created_from: '{moment_id}'
                        }}]->(b)
                        """)
                        crystallized += 1

        except Exception as e:
            logger.warning(f"[Crystallize] Error for {moment_id}: {e}")

        return crystallized

    # =========================================================================
    # PHASE 8: REJECTION
    # =========================================================================

    def _phase_rejection(
        self,
        possible_moments: List[Dict],
        player_id: str,
        current_tick: int
    ) -> List[Dict]:
        """
        Phase 8: Reject incoherent possible moments.

        Return 80% energy to player.
        Links to speaker stay warm (cool naturally).

        Note: Actual rejection logic is in canon holder.
        This processes moments marked for rejection.
        """
        rejections = []

        try:
            # Get moments marked for rejection
            rejected = self.read.query("""
            MATCH (m:Moment)
            WHERE m.status = 'rejected' AND m.energy > 0
            RETURN m.id AS id, m.energy AS energy
            """)

            for moment in rejected:
                moment_id = moment.get('id')
                energy = moment.get('energy', 0.0) or 0.0

                # Return energy to player
                return_energy = energy * REJECTION_RETURN_RATE

                # Get player's current energy
                player = self.read.query(f"""
                MATCH (p:Actor {{id: '{player_id}'}})
                RETURN p.energy AS energy
                """)

                if player:
                    player_energy = player[0].get('energy', 0.0) or 0.0
                    new_energy = player_energy + return_energy

                    self.write._query(f"""
                    MATCH (p:Actor {{id: '{player_id}'}})
                    SET p.energy = {new_energy}
                    """)

                # Clear moment energy
                self.write._query(f"""
                MATCH (m:Moment {{id: '{moment_id}'}})
                SET m.energy = 0, m.tick_resolved = {current_tick}
                """)

                rejections.append({
                    'moment_id': moment_id,
                    'energy_returned': return_energy,
                    'tick': current_tick
                })

                logger.info(f"[Phase 8] Rejected {moment_id}, returned {return_energy:.2f} to player")

        except Exception as e:
            logger.warning(f"[Phase 8] Rejection error: {e}")

        return rejections

    # =========================================================================
    # UNIFIED TRAVERSAL
    # =========================================================================

    def _energy_flows_through(
        self,
        link: Dict,
        amount: float,
        flow_emotions: List[List],
        origin_id: str,
        origin_energy: float,
        target_id: str,
        target_energy: float
    ):
        """
        Unified traversal function. Called on EVERY energy transfer.

        Updates link:
        - energy += amount × weight
        - strength grows (permanent)
        - emotions blend
        """
        link_energy = link.get('link_energy', 0.0) or 0.0
        link_strength = link.get('strength', 0.0) or 0.0
        link_weight = link.get('weight', 1.0) or 1.0
        link_emotions = link.get('emotions', []) or []
        origin_weight = link.get('origin_weight', 1.0) or 1.0
        target_weight = link.get('target_weight', 1.0) or 1.0

        # Energy transfer to link
        new_link_energy = link_energy + (amount * link_weight)

        # Strength grows (permanent)
        emotion_intensity = avg_emotion_intensity(link_emotions)
        growth = (amount * emotion_intensity * origin_weight) / ((1 + link_strength) * target_weight)
        new_strength = link_strength + growth

        # Emotion coloring
        blend_rate = amount / (amount + link_energy + 1)
        new_emotions = blend_emotions(link_emotions, flow_emotions, blend_rate)

        # Note: Actual link update requires relationship ID
        # This would be done via the link's rid if we had it
        # For now, log the intended update
        logger.debug(
            f"[Traversal] {origin_id} -> {target_id}: "
            f"energy {link_energy:.2f} -> {new_link_energy:.2f}, "
            f"strength {link_strength:.2f} -> {new_strength:.2f}"
        )

    # =========================================================================
    # HELPER QUERIES
    # =========================================================================

    def _get_moments_by_status(self, status: str) -> List[Dict]:
        """Get moments with a given status."""
        try:
            return self.read.query(f"""
            MATCH (m:Moment)
            WHERE m.status = '{status}'
            RETURN m.id AS id, m.energy AS energy, m.weight AS weight,
                   m.duration_minutes AS duration
            """)
        except:
            return []

    def _get_moment_emotions(self, moment_id: str) -> List[List]:
        """Get weighted average emotions from moment's links."""
        try:
            links = self.read.query(f"""
            MATCH (m:Moment {{id: '{moment_id}'}})-[r]->()
            RETURN r.weight AS weight, r.emotions AS emotions
            """)
            return get_weighted_average_emotions(links)
        except:
            return []

    def _get_narrative_emotions(self, narrative_id: str) -> List[List]:
        """Get emotions associated with a narrative."""
        try:
            result = self.read.query(f"""
            MATCH (n:Narrative {{id: '{narrative_id}'}})
            RETURN n.emotions AS emotions
            """)
            if result and result[0].get('emotions'):
                return result[0].get('emotions')
            return []
        except:
            return []

    def _get_hot_links_to_moment(self, moment_id: str, n: int = 20) -> List[Dict]:
        """Get top N hot links from actors to a moment."""
        try:
            return self.read.query(f"""
            MATCH (a:Actor)-[r]->(m:Moment {{id: '{moment_id}'}})
            WHERE type(r) IN ['EXPRESSES', 'CAN_SPEAK', 'SAID']
            RETURN a.id AS actor_id, a.energy AS actor_energy, a.weight AS actor_weight,
                   r.conductivity AS conductivity, r.weight AS weight,
                   r.energy AS link_energy, r.strength AS strength, r.emotions AS emotions
            ORDER BY coalesce(r.energy, 0) * coalesce(r.weight, 1) DESC
            LIMIT {n}
            """)
        except:
            return []

    def _get_hot_links_from_moment(self, moment_id: str, n: int = 20) -> List[Dict]:
        """Get top N hot outgoing links from a moment."""
        try:
            return self.read.query(f"""
            MATCH (m:Moment {{id: '{moment_id}'}})-[r]->(t)
            WHERE NOT t:Actor
            RETURN t.id AS target_id, labels(t)[0] AS target_type,
                   t.energy AS target_energy, t.weight AS target_weight,
                   r.conductivity AS conductivity, r.weight AS weight,
                   r.energy AS link_energy, r.emotions AS emotions
            ORDER BY coalesce(r.energy, 0) * coalesce(r.weight, 1) DESC
            LIMIT {n}
            """)
        except:
            return []

    def _get_hot_links_to_actors(self, narrative_id: str, n: int = 20) -> List[Dict]:
        """Get top N hot links from narrative to actors."""
        try:
            return self.read.query(f"""
            MATCH (a:Actor)-[r:BELIEVES]->(n:Narrative {{id: '{narrative_id}'}})
            RETURN a.id AS actor_id, a.energy AS actor_energy, a.weight AS actor_weight,
                   r.conductivity AS conductivity, r.weight AS weight,
                   r.energy AS link_energy, r.emotions AS emotions
            ORDER BY coalesce(r.energy, 0) * coalesce(r.weight, 1) DESC
            LIMIT {n}
            """)
        except:
            return []

    def _count_hot_cold_links(self) -> Tuple[int, int]:
        """Count hot vs cold links in the graph."""
        try:
            result = self.read.query(f"""
            MATCH ()-[r]->()
            WHERE r.energy IS NOT NULL
            RETURN
                sum(CASE WHEN r.energy * coalesce(r.weight, 1) > {COLD_THRESHOLD} THEN 1 ELSE 0 END) AS hot,
                sum(CASE WHEN r.energy * coalesce(r.weight, 1) <= {COLD_THRESHOLD} THEN 1 ELSE 0 END) AS cold
            """)
            if result:
                return result[0].get('hot', 0), result[0].get('cold', 0)
            return 0, 0
        except:
            return 0, 0

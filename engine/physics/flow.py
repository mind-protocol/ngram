"""
Energy Flow — Unified Traversal and Helpers

Schema v1.2 core physics primitives:
- energy_flows_through(): unified traversal function
- get_hot_links(): top-N link filter
- target_weight_factor(): sqrt(target.weight) reception

EVERY energy transfer must use energy_flows_through() to ensure:
1. Link energy is updated (attention)
2. Link strength grows (permanent depth)
3. Emotions are blended (Hebbian coloring)

DOCS: docs/physics/algorithms/ALGORITHM_Physics_Schema_v1.2_Energy_Physics.md
"""

from typing import List, Dict, Any, Optional, Tuple
from math import sqrt

from engine.physics.constants import (
    COLD_THRESHOLD,
    TOP_N_LINKS,
    EMOTION_BASELINE,
    MAX_EMOTIONS_PER_LINK,
    avg_emotion_intensity,
)
from engine.models.links import blend_emotions


def target_weight_factor(weight: float) -> float:
    """
    Calculate reception factor based on target weight.

    v1.2: Important targets receive more (diminishing returns).

    Args:
        weight: Target node weight (unbounded)

    Returns:
        sqrt(weight) — reception factor
    """
    if weight <= 0:
        return 0.0
    return sqrt(weight)


def energy_flows_through(
    link: Dict[str, Any],
    amount: float,
    flow_emotions: List[List],
    origin_weight: float,
    target_weight: float,
) -> Dict[str, Any]:
    """
    Unified traversal function — MUST be called on EVERY energy transfer.

    Updates link state:
    1. energy: link.energy += amount × link.weight (attention)
    2. strength: grows based on formula (permanent depth)
    3. emotions: blended with flow_emotions (Hebbian coloring)

    Args:
        link: Link dict with energy, strength, weight, emotions fields
        amount: Energy amount flowing through
        flow_emotions: Emotions from the flow [[name, intensity], ...]
        origin_weight: Weight of the origin node
        target_weight: Weight of the target node

    Returns:
        Updated link dict (also modifies in place)

    Formula:
        link.energy += amount × link.weight

        emotion_intensity = avg(link.emotions) or 0.5
        growth = (amount × emotion_intensity × origin_weight) / ((1 + link.strength) × target_weight)
        link.strength += growth

        blend_rate = amount / (amount + link.energy + 1)
        link.emotions = blend(link.emotions, flow_emotions, blend_rate)
    """
    if amount <= 0:
        return link

    link_weight = link.get('weight', 1.0)
    current_energy = link.get('energy', 0.0)
    current_strength = link.get('strength', 0.0)
    current_emotions = link.get('emotions', [])

    # 1. Energy transfer (attention)
    link['energy'] = current_energy + amount * link_weight

    # 2. Strength growth (permanent)
    emotion_intensity = avg_emotion_intensity(current_emotions)
    if target_weight <= 0:
        target_weight = 1.0

    growth = (amount * emotion_intensity * origin_weight) / ((1 + current_strength) * target_weight)
    link['strength'] = current_strength + growth

    # 3. Emotion coloring (Hebbian)
    if flow_emotions:
        blend_rate = amount / (amount + current_energy + 1)
        link['emotions'] = blend_emotions(
            current_emotions,
            flow_emotions,
            blend_rate,
            max_emotions=MAX_EMOTIONS_PER_LINK
        )

    return link


def get_hot_links(
    links: List[Dict[str, Any]],
    n: int = TOP_N_LINKS,
    threshold: float = COLD_THRESHOLD,
) -> List[Dict[str, Any]]:
    """
    Get top-N hot links by energy × weight.

    v1.2: Physics processes only hot links. Cold links stay in graph
    for paths/queries but are excluded from tick computation.

    Args:
        links: List of link dicts with energy and weight fields
        n: Maximum links to return (default TOP_N_LINKS=20)
        threshold: Minimum heat score (default COLD_THRESHOLD=0.01)

    Returns:
        Top N links with heat_score > threshold, sorted by heat_score descending
    """
    # Calculate heat scores
    scored = []
    for link in links:
        energy = link.get('energy', 0.0)
        weight = link.get('weight', 1.0)
        heat_score = energy * weight

        if heat_score > threshold:
            scored.append((link, heat_score))

    # Sort by heat score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Return top N
    return [link for link, score in scored[:n]]


def calculate_flow(
    source_energy: float,
    rate: float,
    link_conductivity: float,
    link_weight: float,
    emotion_factor: float,
) -> float:
    """
    Calculate energy flow amount using unified formula.

    v1.2 unified formula:
        flow = source.energy × rate × conductivity × weight × emotion_factor

    Args:
        source_energy: Energy of the source node
        rate: Base rate (GENERATION_RATE, DRAW_RATE, BACKFLOW_RATE)
        link_conductivity: Link conductivity [0-1]
        link_weight: Link weight (unbounded)
        emotion_factor: Emotion proximity factor

    Returns:
        Flow amount
    """
    return source_energy * rate * link_conductivity * link_weight * emotion_factor


def calculate_received(flow: float, target_weight: float) -> float:
    """
    Calculate energy received by target.

    v1.2: received = flow × sqrt(target.weight)
    Important targets receive more (diminishing returns).

    Args:
        flow: Energy flow amount
        target_weight: Weight of the target node

    Returns:
        Energy received by target
    """
    return flow * target_weight_factor(target_weight)


def cool_link(
    link: Dict[str, Any],
    node_a: Dict[str, Any],
    node_b: Dict[str, Any],
    drain_rate: float = 0.3,
    strength_rate: float = 0.1,
) -> Tuple[Dict[str, Any], float, float]:
    """
    Cool a link by draining energy to nodes and converting to strength.

    v1.2 link cooling (no arbitrary decay):
    1. Drain 30% of energy to connected nodes (50/50 split)
    2. Convert 10% of energy to permanent strength
    3. Total energy reduction = drain + strength conversion

    Args:
        link: Link dict to cool
        node_a: First connected node (modified in place)
        node_b: Second connected node (modified in place)
        drain_rate: Percentage to drain to nodes (default 0.3)
        strength_rate: Percentage to convert to strength (default 0.1)

    Returns:
        (updated_link, energy_to_a, energy_to_b)
    """
    current_energy = link.get('energy', 0.0)
    current_strength = link.get('strength', 0.0)
    current_emotions = link.get('emotions', [])

    if current_energy <= 0:
        return link, 0.0, 0.0

    # Calculate drain
    drain = current_energy * drain_rate

    # Split to nodes
    energy_to_a = drain * 0.5
    energy_to_b = drain * 0.5

    # Update node energies
    node_a['energy'] = node_a.get('energy', 0.0) + energy_to_a
    node_b['energy'] = node_b.get('energy', 0.0) + energy_to_b

    # Convert to strength
    emotion_intensity = avg_emotion_intensity(current_emotions)
    node_a_weight = node_a.get('weight', 1.0)
    node_b_weight = node_b.get('weight', 1.0)

    if node_b_weight <= 0:
        node_b_weight = 1.0

    strength_energy = current_energy * strength_rate
    growth = (strength_energy * emotion_intensity * node_a_weight) / ((1 + current_strength) * node_b_weight)
    link['strength'] = current_strength + growth

    # Reduce energy
    link['energy'] = current_energy - drain - strength_energy

    return link, energy_to_a, energy_to_b


def get_weighted_average_emotions(links: List[Dict[str, Any]]) -> List[List]:
    """
    Calculate weighted average emotions from a list of links.

    Used to get a moment's combined emotions from its connected links.

    Args:
        links: List of link dicts with emotions and weight fields

    Returns:
        Weighted average emotion list [[name, intensity], ...]
    """
    emotion_weights: Dict[str, Tuple[float, float]] = {}  # name -> (sum, weight)

    for link in links:
        link_weight = link.get('weight', 1.0)
        emotions = link.get('emotions', [])

        for emotion in emotions:
            if len(emotion) != 2:
                continue
            name, intensity = emotion[0], float(emotion[1])

            if name in emotion_weights:
                current_sum, current_weight = emotion_weights[name]
                emotion_weights[name] = (current_sum + intensity * link_weight, current_weight + link_weight)
            else:
                emotion_weights[name] = (intensity * link_weight, link_weight)

    # Calculate weighted averages
    result = []
    for name, (total, weight) in emotion_weights.items():
        if weight > 0:
            avg = total / weight
            if avg > 0.01:
                result.append([name, round(avg, 3)])

    # Sort by intensity descending
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:MAX_EMOTIONS_PER_LINK]

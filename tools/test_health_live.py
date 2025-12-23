#!/usr/bin/env python3
"""
Test Health Live - Copy seed graph and run ticks to test health updates.

Usage:
    python tools/test_health_live.py
    python tools/test_health_live.py --ticks 5
    python tools/test_health_live.py --watch
"""

import argparse
import json
import time
import redis
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.physics.tick import GraphTick
from engine.health import get_health_service, get_current_health


def copy_graph(r: redis.Redis, source: str, target: str) -> bool:
    """Copy a graph by dumping and restoring all nodes and edges."""
    print(f"Copying graph '{source}' -> '{target}'...")

    # Delete target if exists
    try:
        r.execute_command('GRAPH.DELETE', target)
        print(f"  Deleted existing '{target}'")
    except:
        pass

    # Get all nodes from source
    nodes_result = r.execute_command('GRAPH.QUERY', source, """
        MATCH (n)
        RETURN id(n) as id, labels(n) as labels, properties(n) as props
    """)

    # Get all edges from source
    edges_result = r.execute_command('GRAPH.QUERY', source, """
        MATCH (a)-[r]->(b)
        RETURN id(a) as src_id, id(b) as tgt_id, type(r) as type, properties(r) as props
    """)

    # Parse nodes
    nodes = []
    if nodes_result and nodes_result[0]:
        for row in nodes_result[0]:
            nodes.append({
                'id': row[0],
                'labels': row[1],
                'props': row[2]
            })

    # Parse edges
    edges = []
    if edges_result and edges_result[0]:
        for row in edges_result[0]:
            edges.append({
                'src_id': row[0],
                'tgt_id': row[1],
                'type': row[2],
                'props': row[3]
            })

    print(f"  Found {len(nodes)} nodes, {len(edges)} edges")

    # Create nodes in target (batch by label)
    id_map = {}  # old_id -> new_id
    for node in nodes:
        labels = node['labels']
        props = node['props']
        label_str = ':'.join(labels) if labels else 'Node'

        # Build props string
        props_str = ', '.join(f"{k}: {json.dumps(v)}" for k, v in props.items()) if props else ''

        cypher = f"CREATE (n:{label_str} {{{props_str}}}) RETURN id(n)"
        try:
            result = r.execute_command('GRAPH.QUERY', target, cypher)
            if result and result[0]:
                new_id = result[0][0][0]
                id_map[node['id']] = new_id
        except Exception as e:
            print(f"  Error creating node: {e}")

    print(f"  Created {len(id_map)} nodes in target")

    # Create edges in target
    edges_created = 0
    for edge in edges:
        src_new = id_map.get(edge['src_id'])
        tgt_new = id_map.get(edge['tgt_id'])

        if src_new is None or tgt_new is None:
            continue

        props = edge['props']
        props_str = ', '.join(f"{k}: {json.dumps(v)}" for k, v in props.items()) if props else ''

        cypher = f"""
            MATCH (a), (b)
            WHERE id(a) = {src_new} AND id(b) = {tgt_new}
            CREATE (a)-[r:{edge['type']} {{{props_str}}}]->(b)
        """
        try:
            r.execute_command('GRAPH.QUERY', target, cypher)
            edges_created += 1
        except Exception as e:
            pass  # Ignore edge errors

    print(f"  Created {edges_created} edges in target")
    print(f"  Graph copy complete!")
    return True


def run_ticks(graph_name: str, num_ticks: int, elapsed_minutes: float = 10.0):
    """Run graph ticks and report health after each."""
    print(f"\nRunning {num_ticks} ticks on '{graph_name}'...")

    tick_engine = GraphTick(graph_name=graph_name)
    health_service = get_health_service()
    health_service.set_context(playthrough_id="test", place_id="test_location")
    health_service.set_speed("x1")

    for i in range(num_ticks):
        print(f"\n--- Tick {i + 1} ---")

        # Run tick
        result = tick_engine.run(elapsed_minutes=elapsed_minutes)

        # Record to health service
        health_service.record_tick(
            tick=i + 1,
            energy_total=result.energy_total,
            completions=result.moments_decayed
        )
        health_service.record_pressure(
            pressure=result.avg_pressure,
            top_edges=[]
        )

        # Record flips as interrupts
        for flip in result.flips:
            health_service.record_interrupt(
                reason="energy_flip",
                moment_id=flip.get('event_id', '')
            )

        # Print tick results
        print(f"  Energy: {result.energy_total:.2f}")
        print(f"  Flips: {len(result.flips)}")
        print(f"  Narratives updated: {result.narratives_updated}")

        # Print health
        health = get_current_health()
        print(f"\n  Health Status: {health['status']['state']} (score: {health['status']['score']})")
        print(f"  Runner: tick={health['runner']['tick']}, speed={health['runner']['speed']}")
        print(f"  Pressure: {health['pressure']['contradiction']:.2f}")

        time.sleep(0.5)

    print("\n" + "=" * 50)
    print("FINAL HEALTH STATE:")
    print(json.dumps(get_current_health(), indent=2))


def watch_health(interval: float = 2.0):
    """Watch health updates in real-time."""
    print(f"Watching health updates (Ctrl+C to stop)...")
    print("-" * 50)

    try:
        while True:
            health = get_current_health()
            status = health['status']
            runner = health['runner']
            pressure = health['pressure']
            counters = health['counters']

            print(f"\r[{health['ts']}] "
                  f"Status: {status['state']} ({status['score']:.2f}) | "
                  f"Tick: {runner['tick']} | "
                  f"Pressure: {pressure['contradiction']:.2f} | "
                  f"Violations: {counters['query_write_attempts']}/{counters['dmz_violation_attempts']}",
                  end='', flush=True)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description='Test health with live ticks')
    parser.add_argument('--graph', default='seed', help='Graph to run ticks on')
    parser.add_argument('--ticks', type=int, default=3, help='Number of ticks to run')
    parser.add_argument('--elapsed', type=float, default=10.0, help='Elapsed minutes per tick')
    parser.add_argument('--watch', action='store_true', help='Watch health in real-time')
    args = parser.parse_args()

    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    try:
        r.ping()
        print(f"Connected to FalkorDB")
    except:
        print("Error: Cannot connect to Redis/FalkorDB")
        return 1

    # Show graph stats
    result = r.execute_command('GRAPH.QUERY', args.graph,
        "MATCH (n) RETURN labels(n)[0] as type, count(n) as cnt")
    print(f"\nGraph '{args.graph}' contents:")
    if result and result[0]:
        for row in result[0]:
            print(f"  {row[0]}: {row[1]}")

    # Run ticks or watch
    if args.watch:
        watch_health()
    else:
        run_ticks(args.graph, args.ticks, args.elapsed)

    return 0


if __name__ == "__main__":
    exit(main())

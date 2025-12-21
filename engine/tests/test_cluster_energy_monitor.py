from engine.physics.cluster_energy_monitor import ClusterEnergyMonitor


def _gen_nodes(count, value=1.0):
    return {f'node_{i}': value for i in range(count)}


def test_large_cluster_tracking():
    monitor = ClusterEnergyMonitor(large_cluster_threshold=50)
    monitor.record('alpha', _gen_nodes(60))

    snapshots = monitor.large_clusters()
    assert len(snapshots) == 1
    assert snapshots[0].cluster_id == 'alpha'
    assert snapshots[0].total_energy == 60.0


def test_detects_spike_in_cluster():
    monitor = ClusterEnergyMonitor(large_cluster_threshold=5, max_history=4)
    monitor.record('beta', _gen_nodes(5), timestamp=1.0)
    monitor.record('beta', _gen_nodes(5), timestamp=2.0)
    spike_reading = monitor.record('beta', _gen_nodes(5, value=2.0), timestamp=3.0)

    alert = monitor.detect_spike('beta', multiplier=1.3)
    assert alert is not None
    assert alert.total_energy == spike_reading.total_energy
    assert alert.node_count == 5

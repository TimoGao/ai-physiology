from mao.models import BloodPacket
from mao.blood import AIBlood
from mao.runtime import MinimalArtificialOrganism
from mao.experiment import (
    run_all_experiments,
    run_chronic_degradation_experiment,
    run_context_obesity_experiment,
    run_malicious_payload_experiment,
    run_memory_contamination_experiment,
    run_resource_pressure_experiment,
    run_tool_deterioration_experiment,
)


def test_cross_organism_packet_is_rejected():
    blood = AIBlood("a")
    ok = blood.publish(BloodPacket(
        organism_id="b",
        source_organ="x",
        destination_scope="organism",
        payload_type="test",
        body={},
    ))
    assert ok is False
    assert blood.dropped == 1


def test_high_risk_packet_is_quarantined():
    blood = AIBlood("a")
    ok = blood.publish(BloodPacket(
        organism_id="a",
        source_organ="x",
        destination_scope="organism",
        payload_type="test",
        body={},
        risk_level=0.9,
    ))
    assert ok is False
    assert len(blood.quarantine) == 1


def test_memory_maintenance_reduces_duplicates():
    mao = MinimalArtificialOrganism()
    mao.inject_memory_noise(copies=10, confidence=0.8)
    before = len(mao.memory.records)
    mao.memory.maintenance()
    after = len(mao.memory.records)
    assert after < before


def test_homeostasis_enters_alert():
    mao = MinimalArtificialOrganism()
    mao.set_security_risk(0.9)
    snapshot = mao.cycle({"hello": "world"})
    assert snapshot["mode"] == "alert"


def test_context_obesity_experiment_runs():
    result = run_context_obesity_experiment(cycles=20, seed=1, noise_per_cycle=1)
    assert result["experiment"] == "context_obesity"
    assert "baseline" in result and "mao" in result


def test_memory_contamination_experiment_runs():
    result = run_memory_contamination_experiment(cycles=20, seed=1, contamination_interval=3)
    assert result["experiment"] == "memory_contamination"
    assert result["observations"]["contaminants_injected"] > 0


def test_tool_deterioration_experiment_runs():
    result = run_tool_deterioration_experiment(cycles=20, seed=1, interval=5)
    assert result["experiment"] == "tool_deterioration"
    assert result["observations"]["degradation_events"] > 0


def test_resource_pressure_experiment_runs():
    result = run_resource_pressure_experiment(cycles=20, seed=1)
    assert result["experiment"] == "resource_pressure"
    assert result["observations"]["final_pressure"] > 0.9


def test_malicious_payload_experiment_quarantines():
    result = run_malicious_payload_experiment(cycles=20, seed=1, attack_interval=4)
    assert result["experiment"] == "malicious_payload"
    assert result["observations"]["mao_quarantined"] > 0


def test_chronic_degradation_experiment_runs():
    result = run_chronic_degradation_experiment(cycles=30, seed=1)
    assert result["experiment"] == "chronic_degradation"
    assert "suspected_chronic_degradation" in result["observations"]


def test_run_all_experiments():
    result = run_all_experiments(seed=1)
    assert set(result) == {
        "context_obesity",
        "memory_contamination",
        "tool_deterioration",
        "resource_pressure",
        "malicious_payload",
        "chronic_degradation",
    }

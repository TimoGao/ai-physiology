from pathlib import Path

from mao.models import BloodPacket
from mao.blood import AIBlood
from mao.runtime import MinimalArtificialOrganism
from mao.baseline import StrongBaselineAgent
from mao.experiment import (
    run_all_experiments,
    run_chronic_degradation_experiment,
    run_context_obesity_experiment,
    run_malicious_payload_experiment,
    run_memory_contamination_experiment,
    run_resource_pressure_experiment,
    run_tool_deterioration_experiment,
)
from mao.evaluation import (
    export_csv,
    export_json,
    run_experiment_matrix,
    run_repeated_experiment,
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


def test_strong_baseline_has_common_engineering_controls():
    baseline = StrongBaselineAgent(seed=1, cleanup_interval=2)
    assert baseline.ingest_external(
        {"bad": True},
        confidence=0.2,
        risk_level=0.95,
    ) is False
    baseline.inject_memory_noise(copies=3)
    baseline.cycle({"task": 1})
    baseline.cycle({"task": 2})
    assert baseline.rejected_inputs == 1
    assert baseline.maintenance_runs == 1


def test_context_obesity_experiment_runs():
    result = run_context_obesity_experiment(cycles=20, seed=1, noise_per_cycle=1)
    assert result["experiment"] == "context_obesity"
    assert result["baseline_kind"] == "strong"
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


def test_run_all_experiments_with_strong_baseline():
    result = run_all_experiments(seed=1, baseline_kind="strong")
    assert set(result) == {
        "context_obesity",
        "memory_contamination",
        "tool_deterioration",
        "resource_pressure",
        "malicious_payload",
        "chronic_degradation",
    }
    assert all(x["baseline_kind"] == "strong" for x in result.values())


def test_repeated_experiment_builds_summary():
    result = run_repeated_experiment(
        "tool_deterioration",
        seeds=[1, 2, 3],
        baseline_kind="strong",
        cycles=20,
        interval=5,
    )
    assert len(result["runs"]) == 3
    assert "baseline.failures" in result["summary"]
    assert result["summary"]["baseline.failures"]["n"] == 3


def test_experiment_matrix_and_export(tmp_path: Path):
    result = run_experiment_matrix(
        seeds=[1, 2],
        baseline_kinds=("naive", "strong"),
    )
    assert set(result["comparisons"]) == {"naive", "strong"}

    json_path = export_json(result, tmp_path / "results.json")
    csv_path = export_csv(result, tmp_path / "runs.csv")

    assert json_path.exists()
    assert csv_path.exists()
    assert csv_path.read_text(encoding="utf-8-sig").startswith("")


def test_naive_baseline_still_supported():
    result = run_context_obesity_experiment(
        cycles=10,
        seed=1,
        noise_per_cycle=1,
        baseline_kind="naive",
    )
    assert result["baseline_kind"] == "naive"

from mao.experiment_v05 import (
    SCENARIOS,
    VARIANTS,
    run_matrix,
    run_one,
)


def test_same_reliability_substrate_keeps_tool_outcomes_comparable():
    a = run_one("tool_deterioration", "reliability_only", 3)
    b = run_one("tool_deterioration", "reliability_plus_physiology", 3)
    assert a["task_success_rate"] == b["task_success_rate"]
    assert a["reliability.retries"] == b["reliability.retries"]
    assert a["reliability.fallback_calls"] == b["reliability.fallback_calls"]


def test_physiology_does_not_bypass_security_filter():
    a = run_one("malicious_payload", "reliability_only", 2)
    b = run_one("malicious_payload", "reliability_plus_physiology", 2)
    assert a["blocked_payloads"] > 0
    assert b["blocked_payloads"] > 0


def test_physiology_can_improve_context_health_without_changing_reliability():
    a = run_one("context_obesity", "reliability_only", 1)
    b = run_one("context_obesity", "reliability_plus_physiology", 1)
    assert b["memory_integrity"] >= a["memory_integrity"]


def test_v05_matrix_shape():
    result = run_matrix(seeds=[0, 1])
    assert len(result["runs"]) == len(SCENARIOS) * len(VARIANTS) * 2
    assert result["paired_effects"]

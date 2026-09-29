from mao.experiment_v04 import (
    CONFIGS,
    SCENARIOS,
    VARIANTS,
    make_trace,
    run_matrix,
    run_one,
)


def test_trace_is_deterministic():
    a = make_trace("chronic_degradation", 3, 40)
    b = make_trace("chronic_degradation", 3, 40)
    assert a.tool_uniforms == b.tool_uniforms
    assert a.contamination_flags == b.contamination_flags
    assert a.resource_pressure == b.resource_pressure


def test_all_variants_run():
    for variant in VARIANTS:
        result = run_one("memory_contamination", variant, 1)
        assert result["variant"] == variant
        assert 0.0 <= result["task_success_rate"] <= 1.0


def test_ablation_configs_are_distinct():
    assert CONFIGS["mao_full"].use_blood is True
    assert CONFIGS["mao_no_blood"].use_blood is False
    assert CONFIGS["mao_no_homeostasis"].use_homeostasis is False
    assert CONFIGS["mao_no_vital_signs"].use_vital_signs is False
    assert CONFIGS["mao_no_organ_health"].use_organ_health is False


def test_matrix_shape():
    result = run_matrix(seeds=[0, 1])
    expected = len(SCENARIOS) * len(VARIANTS) * 2
    assert len(result["runs"]) == expected
    assert result["paired_effects"]


def test_malicious_payload_is_blocked_by_both_fair_filters():
    baseline = run_one("malicious_payload", "engineering_baseline", 0)
    mao = run_one("malicious_payload", "mao_full", 0)
    assert baseline["blocked_or_quarantined"] > 0
    assert mao["blocked_or_quarantined"] > 0


def test_no_homeostasis_allows_more_context_duplication():
    full = run_one("context_obesity", "mao_full", 0)
    no_homeostasis = run_one("context_obesity", "mao_no_homeostasis", 0)
    assert no_homeostasis["duplicate_ratio"] >= full["duplicate_ratio"]

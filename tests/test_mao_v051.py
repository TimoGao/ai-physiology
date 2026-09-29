from mao.longitudinal_v051 import (
    AdaptiveMonitoringBaseline,
    PhysiologyMonitor,
    make_trace,
    run_benchmark,
)


def test_trace_is_deterministic():
    a = make_trace(3, cycles=80, degraded=True)
    b = make_trace(3, cycles=80, degraded=True)
    assert a.memory_integrity == b.memory_integrity
    assert a.future_failure == b.future_failure


def test_healthy_and_degraded_traces_are_distinct():
    a = make_trace(7, cycles=80, degraded=True)
    b = make_trace(7, cycles=80, degraded=False)
    assert a.memory_integrity != b.memory_integrity


def test_monitors_run():
    trace = make_trace(1, cycles=80, degraded=True)
    adaptive = AdaptiveMonitoringBaseline()
    phys = PhysiologyMonitor()
    for i in range(80):
        sample = {
            "mi": trace.memory_integrity[i],
            "tr": trace.tool_reliability[i],
            "rp": trace.resource_pressure[i],
            "cs": trace.context_saturation[i],
            "er": trace.error_rate[i],
        }
        adaptive.observe(i, sample)
        phys.observe(i, sample)
    assert adaptive.scores
    assert phys.scores
    assert 0.0 <= phys.debt <= 1.0
    assert 0.0 <= phys.reserve <= 1.0


def test_benchmark_shape():
    result = run_benchmark(seeds=range(5), cycles=80)
    assert len(result["evaluation_rows"]) == 20
    assert len(result["summary"]) == 2

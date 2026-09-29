from mao.models import BloodPacket
from mao.blood import AIBlood
from mao.runtime import MinimalArtificialOrganism
from mao.experiment import run_chronic_degradation_experiment


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


def test_experiment_runs():
    result = run_chronic_degradation_experiment(cycles=30, seed=1)
    assert result["experiment"] == "chronic_degradation"
    assert "baseline" in result and "mao" in result

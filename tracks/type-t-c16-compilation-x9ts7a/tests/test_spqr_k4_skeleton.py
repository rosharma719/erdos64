from verifier import spqr_k4_skeleton


def test_k4_census_executes_once(capsys, monkeypatch):
    calls = 0
    original = spqr_k4_skeleton.search_reducible_configurations

    def counted(candidate_spectra):
        nonlocal calls
        calls += 1
        return original(candidate_spectra)

    monkeypatch.setattr(
        spqr_k4_skeleton, "search_reducible_configurations", counted
    )
    result = spqr_k4_skeleton.run_all()
    output = capsys.readouterr().out
    assert calls == 1
    assert output.count("=== Bounded search over small virtual-edge spectra ===") == 1
    assert result["base"]["total"] == 117_649
    assert len(result["base"]["clean"]) == 5_525
    assert result["o7"]["survivors"] == 4_717


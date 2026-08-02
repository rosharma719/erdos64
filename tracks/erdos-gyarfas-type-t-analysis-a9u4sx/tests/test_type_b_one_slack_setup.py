import hashlib
import json
from pathlib import Path

from verifier.type_b_one_slack_setup import EXPECTED_GRAPHS, EXPECTED_SHA256


ROOT = Path(__file__).resolve().parents[1]


def test_one_slack_extremal_input_is_frozen():
    path = ROOT / "data/c48_n19e29.s6"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED_SHA256
    assert len(path.read_bytes().splitlines()) == EXPECTED_GRAPHS


def test_one_slack_extremal_layer_is_empty():
    report = json.loads(
        (ROOT / "data/type_b_one_slack_extremal_certificate.json").read_text()
    )
    assert report["degree_two_histogram"] == {
        "3": 9,
        "4": 61,
        "5": 122,
        "6": 92,
        "7": 19,
        "8": 1,
    }
    assert report["graphs_with_at_most_two_degree_two_vertices"] == 0
    assert report["unresolved"] == "the 28-edge remainder layer"

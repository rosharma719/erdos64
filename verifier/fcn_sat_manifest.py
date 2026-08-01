#!/usr/bin/env python3
"""Build the reproducibility manifest for the FC-N SAT existence run.

Mirrors the manifest convention already used by the geng pipelines
(`manifests/F12_order12_manifest.json`): SHA-256 of every script that
participated, the solver/library versions, and the per-instance verdicts.

Usage:
    python verifier/fcn_sat_manifest.py RESULT_JSON [RESULT_JSON ...] \
        --out manifests/FCN_sat_existence_manifest.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS = [
    "verifier/fcn_sat_existence.py",
    "verifier/fcn_cpsat_existence.py",
    "verifier/test_fcn_sat_existence.py",
    "verifier/cycle_detect.py",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def versions() -> dict:
    out = {"python": platform.python_version()}
    for mod in ("pysat", "networkx", "ortools"):
        try:
            m = __import__(mod)
            out[mod] = getattr(m, "__version__", "unknown")
        except Exception as exc:  # pragma: no cover
            out[mod] = f"unavailable: {exc}"
    try:
        out["nauty_geng"] = subprocess.run(
            ["nauty-geng", "--help"], capture_output=True, text=True
        ).stderr.splitlines()[0].strip()
    except Exception as exc:  # pragma: no cover
        out["nauty_geng"] = f"unavailable: {exc}"
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("results", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--root", type=Path, default=Path("."))
    args = ap.parse_args()

    records = []
    for p in args.results:
        data = json.loads(p.read_text())
        records.extend(data if isinstance(data, list) else [data])

    manifest = {
        "experiment": "FCN-sat-existence",
        "method": "direct SAT graph-existence search (edge variables + eager C4 "
                  "+ lazy CEGAR C8 + lazy vertex-cut 2-connectivity + "
                  "transposition lex symmetry breaking)",
        "soundness_note": "every clause added, eager or lazy, is satisfied by "
                          "every genuine solution of the predicate; therefore "
                          "UNSAT of the accumulated formula proves nonexistence.",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checksums": {s: sha256(args.root / s) for s in SCRIPTS
                      if (args.root / s).exists()},
        "versions": versions(),
        "results": sorted(
            ({k: r.get(k) for k in (
                "n", "dx", "status", "solver", "symbreak", "require_2conn",
                "forbidden", "min_internal_degree", "edge_vars", "base_clauses",
                "lazy_cycle_clauses", "lazy_cut_clauses", "lazy_block_clauses",
                "iterations", "elapsed_seconds")}
             for r in records),
            key=lambda r: (r.get("dx") or 0, r.get("n") or 0),
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    print(f"wrote {args.out} with {len(manifest['results'])} result records")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cross-check the FC-N SAT verdicts across solver backends and symmetry-break
settings.

The prospective UNSAT verdicts rest on a CDCL solver's word. This script
re-decides the same instances with

  * several different CDCL implementations (glucose42, minisat22, mergesat3,
    maplecm, cadical195), and
  * symmetry breaking both on and off,

so that a verdict is only reported as agreed if independent search engines --
and a run that does not restrict the search space at all -- reach it too.

Usage:
    python verifier/fcn_sat_crosscheck.py --n 16 17 18 --dx 2 --time-limit 3600
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fcn_sat_existence import search  # noqa: E402

BACKENDS = ["glucose42", "minisat22", "mergesat3", "maplecm", "cadical195"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", nargs="+", type=int, required=True)
    ap.add_argument("--dx", type=int, default=2, choices=(1, 2))
    ap.add_argument("--time-limit", type=float, default=3600.0)
    ap.add_argument("--backends", nargs="+", default=BACKENDS)
    ap.add_argument("--also-no-symbreak", action="store_true")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    rows = []
    print(f"{'n':>4} {'backend':>12} {'symbrk':>7} {'status':>8} {'iters':>8} "
          f"{'cyccl':>9} {'secs':>10}")
    for n in args.n:
        configs = [(b, True) for b in args.backends]
        if args.also_no_symbreak:
            configs += [(b, False) for b in args.backends]
        verdicts = set()
        for backend, sb in configs:
            t0 = time.time()
            r = search(n, args.dx, time_limit=args.time_limit,
                       symbreak=sb, solver_name=backend)
            rows.append(r)
            verdicts.add(r["status"])
            print(f"{n:>4} {backend:>12} {str(sb):>7} {r['status']:>8} "
                  f"{r['iterations']:>8} {r['lazy_cycle_clauses']:>9} "
                  f"{time.time() - t0:>10.2f}", flush=True)
            if args.out:
                Path(args.out).write_text(json.dumps(rows, indent=2, default=str))
        decisive = verdicts - {"TIMEOUT"}
        if len(decisive) > 1:
            print(f"  *** n={n}: BACKENDS DISAGREE {sorted(verdicts)} -- "
                  f"do not trust this order ***")
        else:
            print(f"  n={n}: agreed {sorted(decisive) or ['(all TIMEOUT)']}"
                  f"{' (some TIMEOUT)' if 'TIMEOUT' in verdicts else ''}")
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=2, default=str))


if __name__ == "__main__":
    main()

"""
Automated batch-reactive constraint completion for the A5-permutation lift of
base0_markstroem. Loop: solve -> independently audit the literal lift for
every forbidden length up to 64 -> for every violation found, derive the
exact base-walk/word/shift-point cut and add it -> re-solve (warm-started
from the previous assignment) -> repeat.

This automates and speeds up exactly the manual "find one bad cycle, patch
one cut" process from the earlier report, but does it in a tight loop with
full audits (not just the first violation found) and warm starts.
"""
import subprocess
import sys
import time

sys.path.insert(0, ".")
sys.path.insert(0, "/home/user/erdos64/verifier")
from lift_lib import BaseGraph, build_lift, lift_witness_to_walk, IDENT
import cycle_detect as cd

SOLVER = "./a5_breakout_solver_v2"
BASE_MAT = "base0_markstroem.mat"
FORBIDDEN = (4, 8, 16, 32, 64)


def parse_found(text):
    assignment = {}
    lines = [l for l in text.splitlines() if l.strip() and not l.startswith("FOUND")]
    edges = {}
    for line in lines:
        parts = line.split()
        u, v = int(parts[0]), int(parts[1])
        perm = tuple(int(x) for x in parts[2:7])
        edges[(u, v) if u < v else (v, u)] = perm
    return edges


def run_solver(cuts_path, warm_path, seed, timeout=120):
    proc = subprocess.run(
        [SOLVER, BASE_MAT, cuts_path, warm_path, str(seed)],
        capture_output=True, text=True, timeout=timeout,
    )
    return proc.stdout, proc.stderr, proc.returncode


def write_cuts(path, cuts):
    with open(path, "w") as f:
        for sh, word in cuts:
            f.write(str(sh) + " " + " ".join(str(z) for z in word) + "\n")


def main():
    bg = BaseGraph()
    cuts = []
    with open("cuts16.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = list(map(int, line.split()))
            cuts.append((parts[0], parts[1:]))
    seen_cuts = set((sh, tuple(w)) for sh, w in cuts)

    warm_path = "auto_warm.txt"
    open(warm_path, "w").close()  # empty first
    cuts_path = "auto_cuts.txt"

    t0 = time.time()
    for it in range(60):
        write_cuts(cuts_path, cuts)
        out = None
        for attempt in range(4):
            seed = 42 if (it == 0 and attempt == 0) else 1000 + it * 10 + attempt
            timeout = 900 if it == 0 else 300
            try:
                out, err, rc = run_solver(cuts_path, warm_path, seed=seed, timeout=timeout)
            except subprocess.TimeoutExpired:
                print(f"[iter {it} attempt {attempt}] TIMEOUT after {timeout}s (seed={seed}) with {len(cuts)} cuts, retrying")
                out = None
                continue
            if "FOUND" in out:
                break
            print(f"[iter {it} attempt {attempt}] solver reported NO solution (rc={rc}); "
                  f"last stderr: {err.strip().splitlines()[-2:] if err.strip() else '(none)'}")
            out = None
        if out is None:
            print(f"[iter {it}] exhausted retries with {len(cuts)} cuts -- stopping")
            break

        edge_perms = parse_found(out)
        assignment = {}
        for e, perm in edge_perms.items():
            var = bg.vo[bg.eid[e]]
            assignment[var] = perm

        g = build_lift(bg, assignment)
        violations = []
        for L in FORBIDDEN:
            if cd.has_cycle_len_dfs(g, L):
                w = cd.find_cycle_len_dfs(g, L)
                violations.append((L, w))

        elapsed = time.time() - t0
        if not violations:
            print(f"[iter {it}] CLEAN through C64! {elapsed:.1f}s elapsed, {len(cuts)} cuts.")
            with open("SOLUTION_found.txt", "w") as f:
                f.write(out)
            print("Wrote SOLUTION_found.txt -- this is a genuine candidate counterexample.")
            return

        print(f"[iter {it}] {elapsed:.1f}s: violations at lengths "
              f"{[L for L, _ in violations]} with {len(cuts)} cuts")

        new_cuts = 0
        for L, witness in violations:
            walk, sh = lift_witness_to_walk(witness)
            word = bg.word(walk)
            key = (sh, tuple(word))
            if key not in seen_cuts:
                cuts.append((sh, word))
                seen_cuts.add(key)
                new_cuts += 1
        if new_cuts == 0:
            print(f"[iter {it}] all violations already covered by existing cuts but still "
                  f"present -- inconsistency, stopping")
            break

        # warm-start the next attempt from this iteration's assignment
        with open(warm_path, "w") as f:
            f.write(out)

    print(f"auto_repair finished after {time.time()-t0:.1f}s, {len(cuts)} total cuts, no clean result yet")


if __name__ == "__main__":
    main()

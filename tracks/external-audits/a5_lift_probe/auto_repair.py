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

# Repo-root resolution added 2026-08-18 during consolidation: these
# scripts moved out of external_review/ and previously hard-coded an
# absolute home directory.  Resolve relative to this file instead.
import os
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ".")
sys.path.insert(0, os.path.join(_REPO_ROOT, "verifier"))
from lift_lib import BaseGraph, build_lift, lift_witness_to_walk, IDENT
import cycle_detect as cd

SOLVER = "./a5_breakout_solver_v2"
K3_SOLVER = "./a5_point_repair_k3"
FORBIDDEN = (4, 8, 16, 32, 64)


def run_k3(base_mat, cuts_path, warm_path, timeout=300):
    try:
        proc = subprocess.run(
            [K3_SOLVER, base_mat, cuts_path, warm_path],
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None
    if "FOUND" not in proc.stdout:
        return None
    return proc.stdout


def write_mat(edges_path, mat_path):
    with open(edges_path) as f:
        header = f.readline().split()
        n, m = int(header[0]), int(header[1])
        mat = [[0] * n for _ in range(n)]
        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v = map(int, line.split())
            mat[u][v] = mat[v][u] = 1
    with open(mat_path, "w") as f:
        for row in mat:
            f.write(" ".join(map(str, row)) + "\n")


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


def run_solver(base_mat, cuts_path, warm_path, seed, timeout=120):
    proc = subprocess.run(
        [SOLVER, base_mat, cuts_path, warm_path, str(seed)],
        capture_output=True, text=True, timeout=timeout,
    )
    return proc.stdout, proc.stderr, proc.returncode


def write_cuts(path, cuts):
    with open(path, "w") as f:
        for sh, word in cuts:
            f.write(str(sh) + " " + " ".join(str(z) for z in word) + "\n")


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "base0_markstroem"
    edges_path = f"{name}.edges"
    mat_path = f"{name}.mat"
    initial_cuts_path = sys.argv[2] if len(sys.argv) > 2 else None
    write_mat(edges_path, mat_path)
    bg = BaseGraph(edges_path)
    cuts = []
    if initial_cuts_path:
        with open(initial_cuts_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = list(map(int, line.split()))
                cuts.append((parts[0], parts[1:]))
    seen_cuts = set((sh, tuple(w)) for sh, w in cuts)

    warm_path = sys.argv[3] if len(sys.argv) > 3 else f"auto_warm_{name}.txt"
    if len(sys.argv) <= 3:
        open(warm_path, "w").close()  # fresh run: start with an empty warm-start
    # if a warm_path was explicitly given (continuation), preserve its content --
    # do NOT truncate it (this was a real bug: it silently discarded a prepared
    # near-solution warm-start on every continuation run).
    cuts_path = f"auto_cuts_{name}.txt"
    solution_path = f"SOLUTION_found_{name}.txt"
    log_prefix = name

    t0 = time.time()
    for it in range(60):
        write_cuts(cuts_path, cuts)
        out = None
        for attempt in range(4):
            seed = 42 if (it == 0 and attempt == 0) else 1000 + it * 10 + attempt
            timeout = 900 if it == 0 else 300
            try:
                out, err, rc = run_solver(mat_path, cuts_path, warm_path, seed=seed, timeout=timeout)
            except subprocess.TimeoutExpired:
                print(f"[{log_prefix} iter {it} attempt {attempt}] TIMEOUT after {timeout}s (seed={seed}) with {len(cuts)} cuts, retrying")
                out = None
                continue
            if "FOUND" in out:
                break
            print(f"[{log_prefix} iter {it} attempt {attempt}] solver reported NO solution (rc={rc}); "
                  f"last stderr: {err.strip().splitlines()[-2:] if err.strip() else '(none)'}")
            out = None
        if out is None:
            print(f"[{log_prefix} iter {it}] random-restart exhausted with {len(cuts)} cuts, "
                  f"trying exhaustive k3-repair fallback")
            out = run_k3(mat_path, cuts_path, warm_path, timeout=300)
            if out is None:
                print(f"[{log_prefix} iter {it}] k3-repair also found nothing with {len(cuts)} cuts -- stopping")
                break
            print(f"[{log_prefix} iter {it}] k3-repair found a fix")

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
            print(f"[{log_prefix} iter {it}] CLEAN through C64! {elapsed:.1f}s elapsed, {len(cuts)} cuts.")
            with open(solution_path, "w") as f:
                f.write(out)
            print(f"Wrote {solution_path} -- this is a genuine candidate counterexample.")
            return

        print(f"[{log_prefix} iter {it}] {elapsed:.1f}s: violations at lengths "
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
            print(f"[{log_prefix} iter {it}] all violations already covered by existing cuts but still "
                  f"present -- inconsistency, stopping")
            break

        # warm-start the next attempt from this iteration's assignment
        with open(warm_path, "w") as f:
            f.write(out)

    print(f"[{log_prefix}] auto_repair finished after {time.time()-t0:.1f}s, {len(cuts)} total cuts, no clean result yet")


if __name__ == "__main__":
    main()

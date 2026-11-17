---
id: c-rooted-robustness-hard-instances
title: "All known 4/8/16-free cubic graphs are root-robust"
kind: claim
label: "COMPUTATIONALLY VERIFIED"
topics: ["run-2026-11"]
doc_status: active
date: 2026-11-17
summary: "Every vertex is avoided by a dyadic cycle in: all {C4,C8}-free cubic graphs on 24 and 26 vertices; 48 C8-free girth-5 graphs on 30 vertices; 100 large vertex-transitive survivors; 18 {C4,C8,C16}-free cubic graphs on 82–126 vertices (via C32); the 370-vertex {C4..C32}-free graph (via C64); the 26,…"
evidence: ["kb/runs/2026-11-16-dossier/passes/14_rooted_stress_test/results/wit_hard.txt", "kb/runs/2026-11-16-dossier/passes/14_rooted_stress_test/results/external_sha256.txt"]
depends_on: []
---

# All known 4/8/16-free cubic graphs are root-robust

## Statement

Every vertex is avoided by a dyadic cycle in: all {C4,C8}-free cubic graphs on 24 and 26 vertices; 48 C8-free girth-5 graphs on 30 vertices; 100 large vertex-transitive survivors; 18 {C4,C8,C16}-free cubic graphs on 82–126 vertices (via C32); the 370-vertex {C4..C32}-free graph (via C64); the 26,550-vertex {C4..C64}-free graph (via C128). Witness cycles independently verified.

## Evidence

- `kb/runs/2026-11-16-dossier/passes/14_rooted_stress_test/results/wit_hard.txt`
- `kb/runs/2026-11-16-dossier/passes/14_rooted_stress_test/results/external_sha256.txt`

## Caveats

Input graphs come from github.com/mcolsen/erdos-gyarfas (commit 9a6cf9b), referenced by SHA-256, not vendored.

## History

- 2026-11-17: created from the November 2026 run.

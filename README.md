# erdos64 — research knowledge base on the Erdős–Gyárfás conjecture

> **Conjecture (Erdős–Gyárfás, 1995; Erdős Problems #64).** Every finite simple graph
> with minimum degree ≥ 3 contains a cycle whose length is a power of two.
>
> **Status: OPEN.** This repository records partial results, computations,
> audits and failed approaches. Every claim is labelled. Nothing here resolves
> the conjecture.

## Start here

| If you are… | Read |
|---|---|
| new to the project | [`kb/STATE.md`](kb/STATE.md): one-page state of knowledge, frontier, open problems, dead ends |
| looking for a document | [`kb/INDEX.md`](kb/INDEX.md), or the machine-readable [`kb/index.json`](kb/index.json) |
| an LLM agent | [`AGENTS.md`](AGENTS.md) and [`llms.txt`](llms.txt) |
| contributing | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

## Layout

```
kb/                     the knowledge base (all indexed markdown)
  STATE.md              curated state of knowledge — read first
  INDEX.md, index.json  generated index of every document
  claims/               one result per file (label, statement, evidence)
  open/                 one open problem per file
  core/                 living ledgers: proof.md, lemmas.md, plan.md, literature.md,
                        verification_status.md, experiments.md, manuscript.md, RETROSPECTIVE.md
  notes/<topic>/        topical notes from the July–October 2026 campaigns
  runs/<date>-<slug>/   dated research runs (e.g. 2026-11-16-dossier)
tracks/                 work streams with code + notes (notes indexed in place)
verifier/ tests/        checkers and test suite
data/ manifests/ logs/  certificates, catalogs, provenance hashes, run logs
tools/kb.py             index / check / resolve / new
```

## Commands

```bash
make setup          # virtualenv + pinned dependencies
make check          # native checkers, syntax, full test suite (includes the kb check)
make kb             # regenerate kb/INDEX.md, kb/index.json, llms.txt
make kb-check       # validate knowledge-base metadata and generated files
python tools/kb.py resolve type_b_one_slack.md   # find a note by its legacy filename
```

Some tests need nauty's `labelg` on `PATH`.

## History

- **July–October 2026:** multi-branch campaigns, consolidated on 18 August 2026. The
  branch topology and what was kept are recorded in `tracks/MANIFEST.md`; the old
  per-file guide is `kb/core/legacy_readme.md`.
- **November 2026:** the research run is in `kb/runs/2026-11-16-dossier/`.
- **17 November 2026:** the repository was reorganized into this layout. Notes keep
  their filenames, and `legacy_path` metadata records where each one used to live.

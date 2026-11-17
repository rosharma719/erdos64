# AGENTS.md — instructions for LLM agents working in this repository

This repository is a research knowledge base on the **Erdős–Gyárfás conjecture**, which
is open. Your job is usually one of three things:
1. answer a question from the knowledge base;
2. extend it with new results;
3. audit existing claims.

## Orientation, in this order

1. **`kb/STATE.md`**: curated state of knowledge. It is short; read all of it.
2. **`kb/index.json`**: every document with `id`, `kind`, `label`, `doc_status`,
   `topics`, `summary`, `path`, `depends_on` and `evidence`. Filter it instead of
   opening files blindly. `kb/INDEX.md` is the same content for humans.
3. **`kb/claims/` and `kb/open/`**: one result or open problem per file. These are the
   atomic units to cite.
4. **`kb/core/proof.md`**: the labelled narrative ledger for July–October.
   `kb/core/verification_status.md` is the row-by-row verification matrix.
5. Topical notes under `kb/notes/<topic>/` and run documents under `kb/runs/`, only as
   needed.

**Resolving legacy references.** Older files, code comments and `manifests/*.json`
refer to notes by bare legacy filename (for example `defect.md`). Use
`python tools/kb.py resolve <name>`, or search `index.json` for `legacy_path`.

## Epistemic rules (non-negotiable)

- **Labels.** Use exactly: PROVED, COMPUTATIONALLY VERIFIED, KNOWN FROM LITERATURE,
  SKETCH, CONJECTURAL, OPEN, DISPROVED. Never upgrade a label without new evidence in
  the repo. Keep legacy qualifiers (`NOVELTY SUPPORTED BY SEARCH`,
  `BOUNDED_INCOMPLETE`, …) verbatim.
- **No claim of resolution.** Do not claim the conjecture is proved or disproved. If
  you believe you have done either, write it up as a claim labelled SKETCH or
  CONJECTURAL and ask for human review.
- **Finite is not universal.** A pattern observed on a special subsequence (for example
  N = 2ᵏ) is not a theorem. This is the most repeated failure mode here; see
  `kb/core/RETROSPECTIVE.md`.
- **Literature.** Record how you verified each citation: read in full, abstract only,
  or secondary quote. Statements known only through a secondary quote must say so.
- **Keep failures.** Disproved and retracted items are kept, with the witness. Do not
  delete them.

## Editing rules (keep pull requests additive)

- **Add, don't rewrite.**
  - New results go in **new files**: `kb/claims/<id>.md`, `kb/open/<id>.md`, a new pass
    under a run, or a new note under `kb/notes/<topic>/`.
  - Scaffold them with `python tools/kb.py new claim --id c-... --title "..."`.
  - Changing an existing claim's label or statement: edit the file **and** append a
    dated line under `## History` explaining why, with evidence. Or create a new claim
    with `supersedes: ["old-id"]`.
- **Never edit hash-locked files.** These are files whose metadata lives in a
  `_meta.json` sidecar with `hash_locked: true`. Their SHA-256 is recorded in
  `manifests/`. Supersede them with a new note instead.
- **Do not edit generated files by hand.** These are `kb/INDEX.md`, `kb/index.json` and
  `llms.txt`. Run `python tools/kb.py index`.
- **Before committing,** run `python tools/kb.py check`. It must print `OK`.
- **Update `kb/STATE.md`** when a result changes the big picture: frontier, the label of
  a headline claim, or a new dead end. Keep it to one page.
- **Code and data** go in `verifier/`, `tests/`, `data/` and `manifests/`. Notes must say
  how to reproduce every computation: command, parameters, counts.

## Environment notes

- Python dependencies: `requirements-dev.txt`.
- Some tests need nauty's `labelg`.
- `tracks/type-t-c16-static-sat/tests/` has a pre-existing module-name clash with
  `verifier/` when the whole tree is collected; run it on its own.
- `kb/runs/*/source_archive/` holds archived scripts that hard-code `/mnt/data` paths.
  It is excluded from test collection.

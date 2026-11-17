---
id: kb-schema
title: "Knowledge-base layout and metadata schema"
kind: guide
topics: ["guide"]
doc_status: active
date: 2026-11-17
summary: "How kb/ is organized, the front-matter schema every document carries, the _meta.json sidecar mechanism for hash-locked or archival files, and the generated indexes."
---

# Knowledge base: layout and schema

## Layout

| Path | Kind | Contents |
|---|---|---|
| `kb/STATE.md` | guide | Curated state of knowledge. **Read first.** |
| `kb/INDEX.md`, `kb/index.json` | generated | Every document with metadata. Built by `tools/kb.py index`. |
| `kb/claims/<id>.md` | claim | One result per file: statement, label, evidence pointers, caveats, history. |
| `kb/open/<id>.md` | open-problem | One open question per file. |
| `kb/core/` | core | Living ledgers from July–October: `proof.md` (labelled narrative), `lemmas.md`, `plan.md`, `literature.md`, `verification_status.md`, `experiments.md`, `manuscript.md`, `RETROSPECTIVE.md`, `legacy_readme.md` (old per-file guide). |
| `kb/notes/<topic>/` | note | Topical research notes from the July–October campaigns. Topics: central-bridge, connectivity, constructions, contraction, defect, finite-frontier, type-a, type-b, type-c, type-t. |
| `kb/runs/<date>-<slug>/` | run, pass, literature, artifact | Self-contained dated research runs, e.g. `2026-11-16-dossier`. |
| `tracks/` | track-note | Work streams that also carry code and tests. Notes are indexed in place. |
| `verifier/`, `tests/`, `data/`, `manifests/`, `logs/` | — | Code, certificates and data. Not part of the indexed knowledge base. |

## Front matter

Every indexed markdown file starts with a front-matter block. It is a strict subset of
YAML: one `key: value` per line, where the value is a bare token or JSON.

```yaml
---
id: type-b-one-slack            # unique, lowercase kebab-case, never reused
title: "One-slack Pi0 bridges"  # human title
kind: note                      # guide|core|claim|open-problem|note|track-note|run|pass|literature|artifact
topics: ["type-b"]              # JSON list
doc_status: active              # active|superseded|audit|historical
date: 2026-07-28                # date added to the repository (YYYY-MM-DD; legacy notes: from git history)
summary: "1–2 sentences an LLM can use to decide whether to open this file."
# optional:
label: "PROVED"                 # required for claim/open-problem; see kb/STATE.md §1
evidence: ["path/to/file.md#section"]   # required for claim/open-problem; paths must exist
depends_on: ["other-id"]        # ids that must exist
supersedes: ["old-id"]
status_line: "verbatim status line from the original file"
legacy_path: "type_b_one_slack.md"      # where the file lived before the 2026-11 reorganization
---
```

## Sidecars for files that must not be edited

Some files must stay byte-identical:
- notes whose SHA-256 is recorded in `manifests/*.json` (`hash_locked: true`);
- uploaded archives;
- packets with their own checksum manifests.

These get metadata from a `_meta.json` file in the same directory, keyed by filename.
A key ending in `/` covers a whole directory, which is then indexed as one artifact.
Never edit a hash-locked file. Add a new note that supersedes it instead.

## Legacy filename references

Older notes, code comments and manifests refer to notes by bare filename, for example
`defect.md` or `type_b_compatibility.md`, as they were before the reorganization. Find
the current path with:

```bash
python tools/kb.py resolve defect.md
```

## Generated files

`kb/INDEX.md`, `kb/index.json` and `/llms.txt` are generated. Never edit them by hand.
After changing any metadata, run:

```bash
python tools/kb.py index
```

`python tools/kb.py check` validates everything; `tests/test_kb.py` runs it.

# Contributing

The knowledge base is designed so that contributions are **additive**. Most pull
requests should only *add* files, plus regenerated indexes. This keeps parallel pull
requests from conflicting, and keeps the history auditable.

## Typical pull requests

### Add a result

```bash
python tools/kb.py new claim --id c-my-lemma --title "Short statement"
# edit kb/claims/c-my-lemma.md:
#   - set label (PROVED / COMPUTATIONALLY VERIFIED / SKETCH / ...)
#   - list evidence paths (the proof note, the computation log)
#   - list depends_on ids
#   - fill in Statement / Evidence / Caveats
python tools/kb.py index && python tools/kb.py check
```

### Record an open problem

```bash
python tools/kb.py new open-problem --id q-my-question --title "..."
```

### Add a research note

```bash
python tools/kb.py new note --topic type-b --id type-b-my-topic --title "..."
```

Topics are folders in `kb/notes/`. Create a new one if nothing fits.

### Add a research run

A run is a series of passes in one session. Create `kb/runs/YYYY-MM-DD-slug/` with:
- a `README.md` (kind `run`), giving the reading order and open items;
- passes `passes/NN_slug.md` (kind `pass`).

Give each new result its own claim file in `kb/claims/`, so it is citable outside the
run.

### Change the status of an existing claim

Edit the claim's `label` and add a dated line under `## History` with the evidence.
For a substantive change of statement, create a new claim with
`supersedes: ["old-id"]` and set the old one's `doc_status: superseded`.

### Literature

Add an entry to the relevant review, or a new `kind: literature` document. State the
verification level for every citation: read in full, abstract only, or secondary.

## Rules

- Never edit hash-locked files (see `kb/README.md`). Supersede them instead.
- Never hand-edit `kb/INDEX.md`, `kb/index.json` or `llms.txt`.
- `python tools/kb.py check` must pass, and `make check` should pass, apart from the
  environment-dependent tests noted in `AGENTS.md`.
- Update `kb/STATE.md` only for big-picture changes, and keep it to one page.
- Computations must be reproducible from the repo: code in `verifier/` or the run
  folder, inputs in `data/`, and the exact command, parameters and counts in the note.

## Merge conflicts in generated files

If two pull requests both regenerate the index, resolve the conflict by re-running
`python tools/kb.py index` on the merged tree.

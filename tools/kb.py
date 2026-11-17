#!/usr/bin/env python3
"""Knowledge-base tool for erdos64.

Every knowledge document carries metadata, either as a front-matter block at the
top of the file or, for hash-locked or archival files, as an entry in a
`_meta.json` sidecar in the same directory. This tool builds the generated
indexes from that metadata and validates it.

Commands
  python tools/kb.py index            regenerate kb/INDEX.md, kb/index.json, llms.txt
  python tools/kb.py check            validate metadata and that generated files are current
  python tools/kb.py resolve NAME     find documents by id, filename, or legacy path
  python tools/kb.py new KIND --id ID --title TITLE [--topic T] [--path DIR]
                                      scaffold a new note / claim / open problem
  python tools/kb.py list [--kind K] [--label L] [--topic T]

Front-matter format (a strict subset of YAML; every value is a bare token or JSON):
  ---
  id: my-note-id
  title: "Human title"
  kind: note
  topics: ["type-b"]
  doc_status: active
  date: 2026-11-17
  summary: "One or two sentences an LLM can use to decide whether to open the file."
  ---
See kb/README.md for the schema.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date as _date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = ["kb", "tracks"]
GENERATED = {
    "kb/INDEX.md": "index_md",
    "kb/index.json": "index_json",
    "llms.txt": "llms_txt",
}
GENERATED_NAMES = {"INDEX.md"}

KINDS = {
    "guide": "orientation documents (state of knowledge, schema, how-tos)",
    "core": "canonical living ledgers (proof, plan, lemmas, literature, verification)",
    "claim": "one result per file, with a label and evidence pointers",
    "open-problem": "one open question per file",
    "note": "topical research notes from the July-October campaigns",
    "track-note": "notes inside tracks/ (work streams that also carry code)",
    "run": "documents of a dated research run (kb/runs/)",
    "pass": "a numbered research pass inside a run",
    "literature": "literature reviews",
    "artifact": "archival bundles, data packets, uploads (indexed, not edited)",
}
DOC_STATUS = {"active", "superseded", "audit", "historical"}
LABELS = {
    "PROVED",
    "COMPUTATIONALLY VERIFIED",
    "KNOWN FROM LITERATURE",
    "SKETCH",
    "CONJECTURAL",
    "OPEN",
    "DISPROVED",
}
REQUIRED = ["id", "title", "kind", "doc_status", "summary"]
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LIST_KEYS = {"topics", "depends_on", "supersedes", "evidence"}


# --------------------------------------------------------------------------- parsing
def parse_front_matter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    meta = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise ValueError(f"bad front-matter line: {raw!r}")
        key, value = raw.split(":", 1)
        value = value.strip()
        if value[:1] in '["{' or value in {"true", "false", "null"} or re.fullmatch(r"-?\d+", value):
            try:
                meta[key.strip()] = json.loads(value)
                continue
            except json.JSONDecodeError:
                pass
        meta[key.strip()] = value
    return meta


def dump_front_matter(meta: dict) -> str:
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, str) and key in {"id", "kind", "doc_status", "date", "label"} and value:
            lines.append(f"{key}: {value}" if key != "label" else f"{key}: {json.dumps(value)}")
        else:
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def tracked(path: Path) -> bool:
    return not any(part.startswith(".") or part == "__pycache__" for part in path.relative_to(ROOT).parts)


def collect() -> tuple[list[dict], list[str]]:
    """Return (documents, problems)."""
    docs, problems = [], []
    covered_dirs: list[Path] = []
    sidecar_files: dict[Path, dict] = {}

    for root in SCAN_ROOTS:
        for sidecar in sorted((ROOT / root).rglob("_meta.json")):
            if not tracked(sidecar):
                continue
            try:
                entries = json.loads(sidecar.read_text())
            except json.JSONDecodeError as exc:
                problems.append(f"{rel(sidecar)}: invalid JSON ({exc})")
                continue
            for name, meta in entries.items():
                target = sidecar.parent / name.rstrip("/")
                if not target.exists():
                    problems.append(f"{rel(sidecar)}: entry {name!r} does not exist")
                    continue
                meta = dict(meta)
                meta["path"] = rel(target) + ("/" if target.is_dir() else "")
                meta["metadata_source"] = rel(sidecar)
                docs.append(meta)
                if target.is_dir():
                    covered_dirs.append(target)
                else:
                    sidecar_files[target] = meta

    for root in SCAN_ROOTS:
        for path in sorted((ROOT / root).rglob("*.md")):
            if not tracked(path) or path in sidecar_files:
                continue
            if rel(path) in GENERATED or path.name in GENERATED_NAMES and path.parent == ROOT / "kb":
                continue
            if any(d in path.parents for d in covered_dirs):
                continue
            try:
                meta = parse_front_matter(path.read_text())
            except ValueError as exc:
                problems.append(f"{rel(path)}: {exc}")
                continue
            if meta is None:
                problems.append(f"{rel(path)}: no front matter and no _meta.json entry")
                continue
            meta["path"] = rel(path)
            meta["metadata_source"] = "front-matter"
            docs.append(meta)
    docs.sort(key=lambda d: (d.get("kind", ""), d.get("path", "")))
    return docs, problems


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def validate(docs: list[dict]) -> list[str]:
    problems = []
    seen: dict[str, str] = {}
    for d in docs:
        where = d.get("path", "?")
        for key in REQUIRED:
            if not d.get(key):
                problems.append(f"{where}: missing required key {key!r}")
        did = d.get("id", "")
        if did and not ID_RE.match(did):
            problems.append(f"{where}: id {did!r} must match {ID_RE.pattern}")
        if did in seen:
            problems.append(f"{where}: duplicate id {did!r} (also {seen[did]})")
        seen[did] = where
        if d.get("kind") and d["kind"] not in KINDS:
            problems.append(f"{where}: unknown kind {d['kind']!r} (allowed: {sorted(KINDS)})")
        if d.get("doc_status") and d["doc_status"] not in DOC_STATUS:
            problems.append(f"{where}: unknown doc_status {d['doc_status']!r}")
        if d.get("date") and not DATE_RE.match(str(d["date"])):
            problems.append(f"{where}: date must be YYYY-MM-DD")
        for key in LIST_KEYS:
            if key in d and not isinstance(d[key], list):
                problems.append(f"{where}: {key} must be a JSON list")
        if d.get("kind") in {"claim", "open-problem"}:
            if d.get("label") not in LABELS:
                problems.append(f"{where}: claims need label in {sorted(LABELS)}")
            if not d.get("evidence"):
                problems.append(f"{where}: claims need a non-empty evidence list")
        elif d.get("label") and d["label"] not in LABELS:
            problems.append(f"{where}: unknown label {d['label']!r}")
        for ev in d.get("evidence", []) or []:
            target = ev.split("#", 1)[0]
            if target.startswith("http"):
                continue
            if not (ROOT / target).exists():
                problems.append(f"{where}: evidence path {target!r} does not exist")
    for d in docs:
        for key in ("depends_on", "supersedes"):
            for ref in d.get(key, []) or []:
                if ref not in seen:
                    problems.append(f"{d.get('path')}: {key} references unknown id {ref!r}")
    return problems


# --------------------------------------------------------------------------- rendering
def link(path: str, base: str) -> str:
    """Relative link from directory `base` (repo-relative) to `path`."""
    depth = 0 if base in ("", ".") else len(Path(base).parts)
    return "../" * depth + path


def one_line(d: dict) -> str:
    return re.sub(r"\s+", " ", str(d.get("summary", ""))).strip()


def row(d: dict, base: str) -> str:
    bits = [d.get("kind", "?"), d.get("doc_status", "?")]
    if d.get("label"):
        bits.insert(0, d["label"])
    if d.get("date"):
        bits.append(str(d["date"]))
    lock = " · hash-locked" if d.get("hash_locked") else ""
    return (f"- `{d.get('id', '?')}` — [{d.get('title', d.get('path'))}]({link(d.get('path', ''), base)}) · "
            f"{' · '.join(map(str, bits))}{lock}  \n  {one_line(d)}")


def group(docs, key):
    out: dict[str, list[dict]] = {}
    for d in docs:
        out.setdefault(key(d), []).append(d)
    return dict(sorted(out.items()))


def index_md(docs: list[dict]) -> str:
    base = "kb"
    lines = [
        "<!-- GENERATED by tools/kb.py index — do not edit by hand; edit front matter / _meta.json instead. -->",
        "# Knowledge-base index",
        "",
        f"{len(docs)} documents. Start with [`STATE.md`](STATE.md) (curated state of knowledge) and "
        "[`../AGENTS.md`](../AGENTS.md) (rules). Machine-readable twin: [`index.json`](index.json).",
        "",
        "Labels on claims: " + ", ".join(sorted(LABELS)) + ".",
        "",
    ]
    order = ["guide", "claim", "open-problem", "core", "literature", "run", "pass", "note", "track-note", "artifact"]
    by_kind = group(docs, lambda d: d.get("kind", "?"))
    for kind in order + sorted(set(by_kind) - set(order)):
        if kind not in by_kind:
            continue
        items = by_kind[kind]
        lines += [f"## {kind} ({len(items)}) — {KINDS.get(kind, '')}", ""]
        if kind in {"note", "track-note"}:
            for topic, sub in group(items, lambda d: (d.get("topics") or ["misc"])[-1]).items():
                lines += [f"### {topic}", ""] + [row(d, base) for d in sub] + [""]
        elif kind in {"claim", "open-problem"}:
            for label, sub in group(items, lambda d: d.get("label", "?")).items():
                lines += [f"### {label}", ""] + [row(d, base) for d in sub] + [""]
        else:
            lines += [row(d, base) for d in items] + [""]
    return "\n".join(lines).rstrip() + "\n"


def index_json(docs: list[dict]) -> str:
    keep = ["id", "title", "kind", "label", "doc_status", "topics", "date", "summary", "path",
            "depends_on", "supersedes", "evidence", "status_line", "legacy_path", "hash_locked",
            "metadata_source"]
    out = [{k: d[k] for k in keep if k in d and d[k] not in ("", [], None)} for d in docs]
    return json.dumps({"schema": "erdos64-kb/1", "documents": out}, ensure_ascii=False, indent=1) + "\n"


def llms_txt(docs: list[dict]) -> str:
    def entry(d):
        return f"- [{d.get('title', d.get('path'))}]({d.get('path', '')}): {one_line(d)}"

    lines = [
        "# erdos64",
        "",
        "> Research knowledge base on the Erdős–Gyárfás conjecture (Erdős Problem #64): every graph with "
        "minimum degree ≥ 3 contains a cycle whose length is a power of two. The conjecture is OPEN; nothing "
        "here proves or disproves it. Every claim carries a label (PROVED, COMPUTATIONALLY VERIFIED, KNOWN "
        "FROM LITERATURE, SKETCH, CONJECTURAL, OPEN, DISPROVED).",
        "",
        "Read AGENTS.md for conventions, then kb/STATE.md for the current state of knowledge. "
        "kb/index.json lists every document with metadata.",
        "",
        "## Start here",
        "- [AGENTS.md](AGENTS.md): rules and workflow for agents working in this repository",
        "- [kb/STATE.md](kb/STATE.md): curated state of knowledge, frontier, open problems, dead ends",
        "- [kb/INDEX.md](kb/INDEX.md): generated index of every document",
        "- [kb/index.json](kb/index.json): the same index, machine-readable",
        "- [CONTRIBUTING.md](CONTRIBUTING.md): how to add knowledge with additive pull requests",
        "",
    ]
    for kind, title in [("open-problem", "Open problems"), ("claim", "Claims"), ("core", "Core ledgers"),
                        ("literature", "Literature"), ("run", "Research runs")]:
        items = [d for d in docs if d.get("kind") == kind]
        if items:
            lines += [f"## {title}"] + [entry(d) for d in items] + [""]
    lines += ["## Optional", "- [kb/INDEX.md](kb/INDEX.md): topical notes, passes, tracks and artifacts", ""]
    return "\n".join(lines)


def render_all(docs):
    return {path: globals()[fn](docs) for path, fn in GENERATED.items()}


# --------------------------------------------------------------------------- commands
def cmd_index(_args) -> int:
    docs, problems = collect()
    problems += validate(docs)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"{len(problems)} problem(s); index not written.", file=sys.stderr)
        return 1
    for path, content in render_all(docs).items():
        (ROOT / path).write_text(content)
    print(f"indexed {len(docs)} documents -> {', '.join(GENERATED)}")
    return 0


def cmd_check(_args) -> int:
    docs, problems = collect()
    problems += validate(docs)
    for path, content in render_all(docs).items():
        target = ROOT / path
        if not target.exists() or target.read_text() != content:
            problems.append(f"{path} is stale — run `python tools/kb.py index`")
    if problems:
        print("\n".join(problems))
        print(f"kb check: {len(problems)} problem(s)")
        return 1
    print(f"kb check: OK ({len(docs)} documents)")
    return 0


def cmd_resolve(args) -> int:
    docs, _ = collect()
    q = args.name.lower()
    hits = [d for d in docs if q in {d.get("id", "").lower(), Path(d.get("path", "")).name.lower(),
                                     str(d.get("legacy_path", "")).lower()}
            or Path(d.get("path", "")).stem.lower() == q]
    if not hits:
        hits = [d for d in docs if q in d.get("path", "").lower() or q in d.get("id", "")]
    for d in hits:
        print(f"{d['id']}\t{d['path']}\t{d.get('kind')}\t{d.get('doc_status')}")
    return 0 if hits else 1


def cmd_list(args) -> int:
    docs, _ = collect()
    for d in docs:
        if args.kind and d.get("kind") != args.kind:
            continue
        if args.label and d.get("label") != args.label:
            continue
        if args.topic and args.topic not in (d.get("topics") or []):
            continue
        print(f"{d['id']}\t{d.get('label', '')}\t{d['path']}\t{one_line(d)[:100]}")
    return 0


TEMPLATES = {
    "claim": ("kb/claims", "## Statement\n\n<precise statement>\n\n## Evidence\n\n<where the proof / computation lives; "
                           "what was checked>\n\n## Caveats\n\n<scope, refereeing status, novelty>\n\n## History\n\n"
                           "- {date}: created.\n"),
    "open-problem": ("kb/open", "## Question\n\n<precise statement>\n\n## Why it matters\n\n<what it unlocks>\n\n"
                                "## Known partial progress\n\n<pointers>\n\n## History\n\n- {date}: created.\n"),
    "note": ("kb/notes", "<body>\n"),
    "pass": ("kb/runs", "<body>\n"),
    "guide": ("kb", "<body>\n"),
    "literature": ("kb", "<body>\n"),
}


def cmd_new(args) -> int:
    if args.kind not in TEMPLATES:
        print(f"kind must be one of {sorted(TEMPLATES)}", file=sys.stderr)
        return 2
    if not ID_RE.match(args.id):
        print(f"id must match {ID_RE.pattern}", file=sys.stderr)
        return 2
    folder, body = TEMPLATES[args.kind]
    directory = ROOT / (args.path or (f"{folder}/{args.topic}" if args.kind == "note" and args.topic else folder))
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{args.id}.md"
    if target.exists():
        print(f"{rel(target)} exists", file=sys.stderr)
        return 1
    today = _date.today().isoformat()
    meta = {"id": args.id, "title": args.title, "kind": args.kind,
            "topics": [args.topic] if args.topic else [], "doc_status": "active", "date": today}
    if args.kind in {"claim", "open-problem"}:
        meta["label"] = "OPEN" if args.kind == "open-problem" else "CONJECTURAL"
        meta["evidence"] = []
        meta["depends_on"] = []
    meta["summary"] = "TODO: one or two sentences."
    target.write_text(dump_front_matter(meta) + f"\n# {args.title}\n\n" + body.format(date=today))
    print(rel(target))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    p = sub.add_parser("resolve"); p.add_argument("name"); p.set_defaults(fn=cmd_resolve)
    p = sub.add_parser("list")
    p.add_argument("--kind"); p.add_argument("--label"); p.add_argument("--topic"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("new")
    p.add_argument("kind"); p.add_argument("--id", required=True); p.add_argument("--title", required=True)
    p.add_argument("--topic"); p.add_argument("--path"); p.set_defaults(fn=cmd_new)
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

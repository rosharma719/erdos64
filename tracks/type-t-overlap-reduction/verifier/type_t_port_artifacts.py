#!/usr/bin/env python3
"""Pack, fetch, and verify external Type-T j=4 certificate artifacts."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path, PurePosixPath

from type_t_port_core_classes import write_inventory


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("manifests/type_t_port_completion_j4_manifest.json")
BUNDLE_INPUTS = (
    Path("data/type_t_port_completion/j4_classes"),
    Path("data/type_t_port_completion/j4_a2_c2_reduced_core.cnf.gz"),
    Path("data/type_t_port_completion/j4_a2_c2_reduced_core.drat.gz"),
    Path("data/type_t_port_completion/j4_a2_c2_reduced_core_analysis.json.gz"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def load_bundle_record(repository: Path) -> dict:
    manifest = json.loads((repository / MANIFEST).read_text())
    record = manifest.get("artifact_bundle")
    if not isinstance(record, dict):
        raise ValueError(f"{MANIFEST} does not contain artifact_bundle metadata")
    return record


@contextlib.contextmanager
def artifact_lock(repository: Path):
    """Serialize fetch/install operations for one working tree."""
    git_directory = repository / ".git"
    lock_path = (
        git_directory / "type_t_port_artifacts.lock"
        if git_directory.is_dir()
        else repository / ".type_t_port_artifacts.lock"
    )
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def require_zstd() -> str:
    executable = shutil.which("zstd")
    if executable is None:
        raise RuntimeError("zstd is required; install it before packing or fetching")
    return executable


def archive_entries(repository: Path):
    for relative_root in BUNDLE_INPUTS:
        root = repository / relative_root
        if not root.exists():
            raise FileNotFoundError(root)
        if root.is_file():
            yield relative_root, root
            continue
        yield relative_root, root
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
            yield path.relative_to(repository), path


def tar_info(relative: Path, source: Path) -> tarfile.TarInfo:
    name = relative.as_posix() + ("/" if source.is_dir() else "")
    info = tarfile.TarInfo(name)
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    info.mtime = 0
    if source.is_dir():
        info.type = tarfile.DIRTYPE
        info.mode = 0o755
    elif source.is_file():
        info.type = tarfile.REGTYPE
        info.mode = 0o644
        info.size = source.stat().st_size
    else:
        raise ValueError(f"unsupported bundle entry: {source}")
    return info


def pack(repository: Path, output: Path) -> dict:
    """Create a deterministic tar.zst containing the exact certificate tree."""
    write_inventory(repository / "data/type_t_port_completion/j4_classes")
    output.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(
        [require_zstd(), "-3", "-T0", "-q", "-f", "-o", str(output)],
        stdin=subprocess.PIPE,
    )
    assert process.stdin is not None
    try:
        with tarfile.open(
            fileobj=process.stdin, mode="w|", format=tarfile.PAX_FORMAT,
        ) as archive:
            for relative, source in archive_entries(repository):
                info = tar_info(relative, source)
                if source.is_file():
                    with source.open("rb") as payload:
                        archive.addfile(info, payload)
                else:
                    archive.addfile(info)
    finally:
        process.stdin.close()
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"zstd exited with status {return_code}")
    return {
        "path": str(output),
        "bytes": output.stat().st_size,
        "sha256": sha256_file(output),
    }


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url, headers={"User-Agent": "erdos64-certificate-fetcher/1"},
    )
    with urllib.request.urlopen(request) as response, destination.open("wb") as target:
        shutil.copyfileobj(response, target, length=1 << 20)


def safe_destination(repository: Path, member_name: str) -> Path:
    relative = PurePosixPath(member_name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe archive path: {member_name}")
    destination = repository.joinpath(*relative.parts).resolve()
    if not destination.is_relative_to(repository.resolve()):
        raise ValueError(f"archive path escapes repository: {member_name}")
    return destination


def extract(repository: Path, archive_path: Path) -> None:
    process = subprocess.Popen(
        [require_zstd(), "-q", "-d", "-c", str(archive_path)],
        stdout=subprocess.PIPE,
    )
    assert process.stdout is not None
    try:
        with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
            for member in archive:
                destination = safe_destination(repository, member.name)
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    source = archive.extractfile(member)
                    if source is None:
                        raise ValueError(f"missing payload for {member.name}")
                    with source, destination.open("wb") as target:
                        shutil.copyfileobj(source, target, length=1 << 20)
                else:
                    raise ValueError(f"unsupported archive member: {member.name}")
    finally:
        process.stdout.close()
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"zstd exited with status {return_code}")


def verify_tree(tree: Path, manifest_repository: Path) -> dict:
    inventory = write_inventory(
        tree / "data/type_t_port_completion/j4_classes",
    )
    manifest = json.loads((manifest_repository / MANIFEST).read_text())
    fixed_paths = (
        "data/type_t_port_completion/j4_a2_c2_reduced_core.cnf.gz",
        "data/type_t_port_completion/j4_a2_c2_reduced_core.drat.gz",
        "data/type_t_port_completion/j4_a2_c2_reduced_core_analysis.json.gz",
    )
    for relative in fixed_paths:
        actual = sha256_file(tree / relative)
        expected = manifest["hashes"][relative]
        if actual != expected:
            raise AssertionError(f"hash mismatch for {relative}: {actual} != {expected}")
    return {
        "status": "PASS",
        "classes": inventory["classes"],
        "files": inventory["files"],
        "inventory_aggregate_sha256": inventory["aggregate_sha256"],
    }


def verify(repository: Path) -> dict:
    return verify_tree(repository, repository)


def expected_targets(repository: Path) -> tuple[list[Path], list[Path]]:
    classes_root = repository / "data/type_t_port_completion/j4_classes"
    classes = json.loads((classes_root / "classes.json").read_text())
    class_directories = [
        classes_root / item["class_id"] for item in classes["classes"]
    ]
    fixed_files = [repository / relative for relative in BUNDLE_INPUTS[1:]]
    return class_directories, fixed_files


def installation_state(repository: Path) -> str:
    class_directories, fixed_files = expected_targets(repository)
    targets = class_directories + fixed_files
    present = [path.exists() for path in targets]
    expected_names = {path.name for path in class_directories}
    classes_root = repository / "data/type_t_port_completion/j4_classes"
    unexpected = [
        path for path in classes_root.glob("class_*")
        if path.name not in expected_names
    ]
    if all(present) and not unexpected:
        return "complete"
    if any(present) or unexpected:
        return "partial"
    return "absent"


def install_staged(repository: Path, staging: Path) -> None:
    destination_classes, destination_fixed = expected_targets(repository)
    source_classes, source_fixed = expected_targets(staging)
    for source, destination in zip(source_classes, destination_classes, strict=True):
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source, destination)
    for source, destination in zip(source_fixed, destination_fixed, strict=True):
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source, destination)


def fetch(repository: Path, local_archive: Path | None, keep_archive: bool) -> dict:
    record = load_bundle_record(repository)
    with artifact_lock(repository):
        state = installation_state(repository)
        if state == "complete":
            result = verify(repository)
            result["installation"] = "already_present"
            return result
        if state == "partial":
            raise RuntimeError(
                "refusing to overwrite a partially populated Type-T artifact tree; "
                "move or remove the ignored partial artifacts before retrying"
            )

        with tempfile.TemporaryDirectory(
            prefix=".type-t-port-artifacts-", dir=repository.parent,
        ) as staging_text:
            staging = Path(staging_text)
            downloaded = local_archive is None
            archive_path = local_archive or staging / record["name"]
            if downloaded:
                download(record["url"], archive_path)
            actual_hash = sha256_file(archive_path)
            if actual_hash != record["sha256"]:
                raise AssertionError(
                    f"bundle hash mismatch: {actual_hash} != {record['sha256']}"
                )
            if archive_path.stat().st_size != record["bytes"]:
                raise AssertionError("bundle byte count does not match the manifest")
            extraction_root = staging / "extracted"
            extraction_root.mkdir()
            extract(extraction_root, archive_path)
            verify_tree(extraction_root, repository)
            install_staged(repository, extraction_root)
            result = verify(repository)
            result["installation"] = "installed"
            if downloaded and keep_archive:
                kept = repository / "data/type_t_port_completion" / record["name"]
                shutil.copy2(archive_path, kept)
                result["archive"] = str(kept)
            return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("pack", "fetch", "verify"))
    parser.add_argument("--repository", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--keep-archive", action="store_true")
    args = parser.parse_args()
    repository = args.repository.resolve()
    if args.command == "pack":
        if args.output is None:
            parser.error("pack requires --output")
        result = pack(repository, args.output.resolve())
    elif args.command == "fetch":
        result = fetch(
            repository, args.archive.resolve() if args.archive else None,
            args.keep_archive,
        )
    else:
        result = verify(repository)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

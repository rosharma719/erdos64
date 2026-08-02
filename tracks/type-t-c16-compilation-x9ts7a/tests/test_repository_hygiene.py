import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def tracked_paths() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode()
    return [ROOT / name for name in output.split("\0") if name]


def test_no_local_state_or_python_cache_is_tracked():
    relative = [path.relative_to(ROOT) for path in tracked_paths()]
    offenders = [
        str(path)
        for path in relative
        if "__pycache__" in path.parts
        or path.suffix in {".pyc", ".pyo"}
        or path.parts[0] in {".claude", ".codex", ".pytest_cache"}
        or path.name == ".DS_Store"
    ]
    assert offenders == []


def test_no_compiled_native_binary_is_tracked():
    executable_magics = {
        b"\x7fELF",
        b"\xcf\xfa\xed\xfe",  # 64-bit Mach-O, little endian
        b"\xfe\xed\xfa\xcf",  # 64-bit Mach-O, big endian
        b"\xca\xfe\xba\xbe",  # universal Mach-O
    }
    offenders = []
    for path in tracked_paths():
        if not path.is_file():
            continue
        with path.open("rb") as source:
            header = source.read(4)
        if header in executable_magics or header[:2] == b"MZ":
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []

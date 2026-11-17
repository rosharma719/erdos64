"""The knowledge base must validate and its generated indexes must be current."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_kb_check_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "kb.py"), "check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

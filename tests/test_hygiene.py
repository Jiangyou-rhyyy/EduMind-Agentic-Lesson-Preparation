import subprocess
import sys


def test_repository_hygiene_scan_passes():
    result = subprocess.run(
        [sys.executable, "scripts/check_repository.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

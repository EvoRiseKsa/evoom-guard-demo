"""Judge-owned invariant executed separately from the repository suite."""

import subprocess
import sys


def test_celsius_boiling_point_protocol() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "tempconv", "c2f", "100"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "212"

import os, subprocess, sys
import pytest
if not (os.environ.get("EVOGUARD_EXEC") or os.environ.get("EVOGUARD_TARGET")):
    pytest.skip("runs only under the EvoOM Guard judge", allow_module_level=True)
def _run(*a):
    py = os.environ.get("EVOGUARD_PYTHON") or sys.executable
    ex = os.environ.get("EVOGUARD_EXEC")
    cmd = [ex, py, "-m", "tempconv", *a] if ex else [py, "-m", "tempconv", *a]
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
def test_c2f_boiling():
    assert _run("c2f", "100") == "212"

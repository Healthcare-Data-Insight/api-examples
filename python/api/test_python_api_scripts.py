import os
import subprocess
import sys
from pathlib import Path

import pytest

API_DIR = Path(__file__).resolve().parent
REPO_ROOT = API_DIR.parents[1]


def _root_api_scripts() -> list[Path]:
    """
    Discover only the top-level Python scripts under python/api.

    This intentionally ignores nested packages such as viewer/, edi_model/,
    and playground/ by looking only one directory deep.
    """
    return sorted(
        path
        for path in API_DIR.glob("*.py")
        if path.is_file()
        and path.name not in {"__init__.py", Path(__file__).name}
    )


@pytest.mark.parametrize("script_path", _root_api_scripts(), ids=lambda path: path.name)
def test_root_api_script_runs_without_failure(script_path: Path) -> None:
    """
    Execute each root-level example script and assert it exits successfully.

    The examples use relative paths such as ../../edi_files/..., so we run them
    from python/api instead of the repository root. We also create the local
    out/ directory up front because the CSV example streams files into it.
    """
    (API_DIR / "out").mkdir(exist_ok=True)

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(API_DIR)
        if not existing_pythonpath
        else os.pathsep.join([str(API_DIR), existing_pythonpath])
    )

    completed = subprocess.run(
        [sys.executable, script_path.name],
        cwd=API_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )

    if completed.returncode != 0:
        pytest.fail(
            "Script exited with a non-zero status.\n"
            f"Script: {script_path}\n"
            f"Exit code: {completed.returncode}\n"
            f"STDOUT:\n{completed.stdout}\n"
            f"STDERR:\n{completed.stderr}"
        )
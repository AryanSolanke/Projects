"""Test configuration for stable local imports and temp paths."""

import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_TEMP_ROOT = PROJECT_ROOT / "test_tmp"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TEST_TEMP_ROOT.mkdir(exist_ok=True)
for env_var in ("TMP", "TEMP", "TMPDIR"):
    os.environ[env_var] = str(TEST_TEMP_ROOT)

tempfile.tempdir = str(TEST_TEMP_ROOT)


@pytest.fixture
def tmp_path():
    """Workspace-local replacement for pytest's blocked tmp_path fixture."""
    path = TEST_TEMP_ROOT / f"case-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


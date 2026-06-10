"""Test setup: import isolation for the kana-code-rpc scripts.

KANA_RPC_DATA_DIR must be set BEFORE state.py is imported, because state.py
resolves DATA_DIR at module level. Subprocess-based tests get their own
isolated dir via the `isolated_data_dir` fixture.
"""
import os
import sys
import tempfile
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent

# Isolate in-process imports of state/presence from the real user data dir
os.environ.setdefault("KANA_RPC_DATA_DIR", tempfile.mkdtemp(prefix="kana-rpc-import-"))

sys.path.insert(0, str(_SCRIPTS_DIR))


@pytest.fixture
def scripts_dir() -> Path:
    return _SCRIPTS_DIR


@pytest.fixture
def isolated_data_dir(tmp_path) -> Path:
    """A fresh data dir for subprocess tests (passed via KANA_RPC_DATA_DIR)."""
    d = tmp_path / "data"
    d.mkdir()
    return d

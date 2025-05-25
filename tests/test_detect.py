import sys
import pytest
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pytadata_entriz._detect import detect


def test_detect_raises(monkeypatch):
    monkeypatch.setitem(sys.modules, "awswrangler", None)
    monkeypatch.setitem(sys.modules, "pandas_gbq", None)
    # reload so detect() re-runs import probe
    importlib.reload(sys.modules["pytadata_entriz._detect"])
    with pytest.raises(RuntimeError):
        detect()

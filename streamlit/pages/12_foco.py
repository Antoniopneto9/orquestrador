"""Entry point wrapper para a página Foco — Pomodoro."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent        # pages/
_STREAMLIT = _HERE.parent                      # streamlit/
_MOD_PATH = _HERE / "12_foco" / "12_foco.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("12_foco_main", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

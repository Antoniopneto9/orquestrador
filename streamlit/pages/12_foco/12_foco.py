"""Entry point for the Foco — Pomodoro page."""

import sys
import importlib.util as _ilu
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))

# Import functions.py by absolute path to avoid sys.path collisions
_fspec = _ilu.spec_from_file_location("foco_functions", _HERE / "functions.py")
_fmod = _ilu.module_from_spec(_fspec)
_fspec.loader.exec_module(_fmod)
renderizar_foco = _fmod.renderizar_foco

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup

st.set_page_config(page_title="Foco — Pomodoro", page_icon="🎯", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("🎯 Foco — Pomodoro")

renderizar_foco()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

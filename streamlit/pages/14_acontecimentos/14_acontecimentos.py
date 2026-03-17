"""Entry point for the Acontecimentos page."""

import sys
import importlib.util as _ilu
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))

_fspec = _ilu.spec_from_file_location("acontecimentos_functions", _HERE / "functions.py")
_fmod = _ilu.module_from_spec(_fspec)
_fspec.loader.exec_module(_fmod)
renderizar_acontecimentos = _fmod.renderizar_acontecimentos

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup

st.set_page_config(page_title="Acontecimentos", page_icon="📰", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📰 Acontecimentos")

renderizar_acontecimentos()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

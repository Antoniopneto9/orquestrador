"""Entry point for the Organização Diária page."""

import sys
import importlib.util as _ilu
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))

_fspec = _ilu.spec_from_file_location("dia_functions", _HERE / "functions.py")
_fmod = _ilu.module_from_spec(_fspec)
_fspec.loader.exec_module(_fmod)
renderizar_organizacao_diaria = _fmod.renderizar_organizacao_diaria

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup

st.set_page_config(page_title="Organização Diária", page_icon="📋", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📋 Organização Diária")

renderizar_organizacao_diaria()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

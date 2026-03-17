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

_foco_path = _HERE.parent / "12_foco" / "functions.py"
_foco_spec = _ilu.spec_from_file_location("foco_functions_dia", _foco_path)
_foco_mod = _ilu.module_from_spec(_foco_spec)
_foco_spec.loader.exec_module(_foco_mod)
renderizar_foco = _foco_mod.renderizar_foco

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup

st.set_page_config(page_title="Meu Dia", page_icon="📋", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📋 Meu Dia")

tab1, tab2 = st.tabs(["📋 Organização Diária", "🎯 Pomodoro"])

with tab1:
    renderizar_organizacao_diaria()

with tab2:
    renderizar_foco()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

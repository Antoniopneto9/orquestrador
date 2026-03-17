"""Entry point for the Correlacao Queixas x Habitos page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "10_correlacao" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("10_correlacao_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
renderizar_correlacao_completa = _mod.renderizar_correlacao_completa

import streamlit as st

st.set_page_config(page_title="Correlação Queixas × Hábitos", page_icon="📈", layout="wide")
st.title("📈 Correlação Queixas × Hábitos")
st.caption("Mostra a relação entre cumprimento de hábitos e nível de sofrimento")

# Orchestrates data loading, computation, validation, and rendering
renderizar_correlacao_completa()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE / "10_correlacao")

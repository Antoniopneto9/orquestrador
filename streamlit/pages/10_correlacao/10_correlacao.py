"""Entry point for the Correlacao Queixas x Habitos page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import renderizar_correlacao_completa

st.set_page_config(page_title="Correlação Queixas × Hábitos", page_icon="📈", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📈 Correlação Queixas × Hábitos")
st.caption("Mostra a relação entre cumprimento de hábitos e nível de sofrimento")

# Orchestrates data loading, computation, validation, and rendering
renderizar_correlacao_completa()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

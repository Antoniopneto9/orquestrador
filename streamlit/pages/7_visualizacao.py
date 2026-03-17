"""Entry point for the Visualizacao Diaria page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "7_visualizacao" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("7_visualizacao_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
renderizar_todas_secoes = _mod.renderizar_todas_secoes

import streamlit as st

st.set_page_config(page_title="Visualização Diária", page_icon="✨", layout="wide")
st.title("✨ Visualização Diária")
st.subheader("Leia com atenção durante a Etapa 3 da meditação")

st.divider()

# Render all 6 identity visualization sections
renderizar_todas_secoes()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE / "7_visualizacao")

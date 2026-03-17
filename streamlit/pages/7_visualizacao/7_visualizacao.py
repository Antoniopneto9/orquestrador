"""Entry point for the Visualizacao Diaria page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import renderizar_todas_secoes

st.set_page_config(page_title="Visualização Diária", page_icon="✨", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("✨ Visualização Diária")
st.subheader("Leia com atenção durante a Etapa 3 da meditação")

st.divider()

# Render all 6 identity visualization sections
renderizar_todas_secoes()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

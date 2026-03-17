"""Entry point for the Meditacao Joe Dispenza page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import (
    get_steps_data,
    renderizar_tabela_etapas,
    renderizar_dicas,
    renderizar_timer,
)

st.set_page_config(page_title="Meditação Joe Dispenza", page_icon="🧘", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("🧘 Meditação Joe Dispenza")
st.caption("Protocolo de 25 minutos para reprogramação neurológica")

# Steps reference table
st.subheader("As 5 Etapas")
steps = get_steps_data()
renderizar_tabela_etapas(steps)

st.divider()

# Practical tips
renderizar_dicas()

st.divider()

# Countdown timer
st.subheader("Timer de Sessão")
renderizar_timer()

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

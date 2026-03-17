"""Entry point for the Revisao Semanal page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import (
    calcular_semana_atual,
    carregar_revisao,
    renderizar_formulario,
    salvar_revisao,
    renderizar_historico,
)

st.set_page_config(page_title="Revisão Semanal", page_icon="📝", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📝 Revisão Semanal")

# Week selector defaulting to current week
current_week = calcular_semana_atual()
selected_week = st.number_input(
    "Semana da temporada",
    min_value=1,
    max_value=52,
    value=current_week,
    step=1,
)

# Load existing review for this week
df, existing_row = carregar_revisao(selected_week)

# Render the review form and collect answers
funcionou, quebrou, ajuste, nota = renderizar_formulario(selected_week, existing_row)

# Save on button click
if st.button("💾 Salvar revisão", type="primary"):
    salvar_revisao(selected_week, funcionou, quebrou, ajuste, nota)
    st.success(f"Revisão da semana {selected_week} salva!")

# Past reviews expander
st.divider()
renderizar_historico(df)

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

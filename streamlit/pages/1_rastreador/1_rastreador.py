"""Entry point for the Rastreador Diario page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/1_rastreador/
_STREAMLIT = _HERE.parents[1]                # streamlit/
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))               # so "from functions import ..." works

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import (
    selecionar_data,
    carregar_habitos,
    renderizar_check_in,
    calcular_totais,
    salvar_check_in,
)

st.set_page_config(page_title="Rastreador Diário", page_icon="📅", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📅 Rastreador Diário")

# Select date clamped to season range
selected_date, date_str, weekday_name, is_weekend = selecionar_data()

if is_weekend:
    st.info("🗓 Final de semana")

# Load habits and any existing answers for this date
habits, new_habits, existing_row = carregar_habitos(selected_date, date_str)
st.subheader(f"Hábitos para {date_str} ({weekday_name})")
st.caption(f"{len(habits)} hábitos ativos neste mês")

# Render habit radio buttons and collect answers
answers = renderizar_check_in(habits, new_habits, existing_row, date_str)

# Show summary metrics
total_yes, total_habits, pct = calcular_totais(answers, habits)
st.divider()
col_a, col_b, col_c = st.columns(3)
col_a.metric("Cumpridos", total_yes)
col_b.metric("Total de hábitos", total_habits)
col_c.metric("Percentual", f"{pct}%")

# Save on button click
if st.button("💾 Salvar", type="primary"):
    salvar_check_in(answers, date_str, total_yes, pct)
    st.success(f"Salvo! {total_yes}/{total_habits} hábitos cumpridos ({pct}%)")

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

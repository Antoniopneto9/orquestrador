"""Entry point for the Dashboard de Habitos page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import (
    carregar_dados,
    calcular_metricas_por_habito,
    renderizar_cards_habitos,
    calcular_total_geral,
    renderizar_grafico,
)

st.set_page_config(page_title="Dashboard de Hábitos", page_icon="📊", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📊 Dashboard de Hábitos")

# Load data — stop early if sheet is empty
df = carregar_dados()
if df.empty:
    st.warning("Nenhum dado encontrado. Preencha o Rastreador para ver o Dashboard.")
    st.stop()

# Per-habit metric cards
st.subheader("Hábitos Fundamentais (8 pilares)")
metrics = calcular_metricas_por_habito(df)
renderizar_cards_habitos(metrics)

# Aggregated totals row
st.subheader("Total Geral")
total_yes, total_no, total_blank, overall_pct = calcular_total_geral(df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total cumpridos", total_yes)
col2.metric("Total falhos", total_no)
col3.metric("Sem resposta", total_blank)
col4.metric("% geral", f"{overall_pct}%")

# Bar chart of % per habit
st.subheader("% de Cumprimento por Hábito")
renderizar_grafico(metrics)

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

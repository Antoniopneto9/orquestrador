"""Entry point for the Dashboard de Habitos page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "2_dashboard" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("2_dashboard_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
carregar_dados = _mod.carregar_dados
calcular_metricas_por_habito = _mod.calcular_metricas_por_habito
renderizar_cards_habitos = _mod.renderizar_cards_habitos
calcular_total_geral = _mod.calcular_total_geral
renderizar_grafico = _mod.renderizar_grafico
carregar_queixas = _mod.carregar_queixas
renderizar_filtros_queixas = _mod.renderizar_filtros_queixas
renderizar_kpis_queixas = _mod.renderizar_kpis_queixas

import streamlit as st


st.set_page_config(page_title="Dashboard de Hábitos", page_icon="📊", layout="wide")
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

st.divider()

# Complaint KPIs
df_queixas = carregar_queixas()
renderizar_kpis_queixas(df_queixas)

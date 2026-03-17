"""Entry point for the Visao Mensal page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "8_mensal" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("8_mensal_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
selecionar_mes, carregar_mes, renderizar_cards_resumo, renderizar_tabela_diaria, renderizar_totais_mes = _mod.selecionar_mes, _mod.carregar_mes, _mod.renderizar_cards_resumo, _mod.renderizar_tabela_diaria, _mod.renderizar_totais_mes

import streamlit as st
from datetime import date

from utils.config import get_habits_for_date

st.set_page_config(page_title="Visão Mensal", page_icon="📆", layout="wide")
st.title("📆 Visão Mensal")

# Month selector
selected_key, year, month, sheet_name = selecionar_mes()

# Load data — stop early if no data for this month
df = carregar_mes(sheet_name)
from utils.config import MONTHS_RANGE

MONTH_LABELS = {
    "2026-03": "Mar/2026", "2026-04": "Abr/2026", "2026-05": "Mai/2026",
    "2026-06": "Jun/2026", "2026-07": "Jul/2026", "2026-08": "Ago/2026",
    "2026-09": "Set/2026", "2026-10": "Out/2026", "2026-11": "Nov/2026",
    "2026-12": "Dez/2026", "2027-01": "Jan/2027", "2027-02": "Fev/2027",
}
if df.empty:
    st.warning(f"Nenhum dado encontrado para {MONTH_LABELS.get(selected_key, selected_key)}.")
    st.stop()

# Determine active habits using the first day of the month as reference
first_day = date(year, month, 1)
active_habits = get_habits_for_date(first_day)

# Summary metrics and progress bar
renderizar_cards_resumo(df)

st.divider()

# Full daily table with color-coded S/N cells
st.subheader("Registros do Mês")
renderizar_tabela_diaria(df, active_habits)

# Monthly habit totals
st.divider()
st.subheader("Totais do Mês")
renderizar_totais_mes(df, active_habits)

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE / "8_mensal")

"""Entry point for the Rastreador Diario page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "1_rastreador" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("1_rastreador_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
selecionar_data, carregar_habitos, renderizar_check_in, calcular_totais, salvar_check_in = _mod.selecionar_data, _mod.carregar_habitos, _mod.renderizar_check_in, _mod.calcular_totais, _mod.salvar_check_in

import streamlit as st


st.set_page_config(page_title="Rastreador Diário", page_icon="📅", layout="wide")
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
render_feedback_box(_HERE / "1_rastreador")

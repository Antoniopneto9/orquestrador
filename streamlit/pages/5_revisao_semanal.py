"""Entry point for the Revisao Semanal page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "5_revisao_semanal" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("5_revisao_semanal_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
calcular_semana_atual, carregar_revisao, renderizar_formulario, salvar_revisao, renderizar_historico = _mod.calcular_semana_atual, _mod.carregar_revisao, _mod.renderizar_formulario, _mod.salvar_revisao, _mod.renderizar_historico

import streamlit as st


st.set_page_config(page_title="Revisão Semanal", page_icon="📝", layout="wide")
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

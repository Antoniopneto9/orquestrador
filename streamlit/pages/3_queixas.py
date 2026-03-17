"""Entry point for the Queixas Diarias page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "3_queixas" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("3_queixas_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
selecionar_data, carregar_queixas_do_dia, calcular_media_existente, renderizar_sliders_por_categoria, salvar_queixas = _mod.selecionar_data, _mod.carregar_queixas_do_dia, _mod.calcular_media_existente, _mod.renderizar_sliders_por_categoria, _mod.salvar_queixas

import streamlit as st


st.set_page_config(page_title="Queixas Diárias", page_icon="🧠", layout="wide")
st.title("🧠 Queixas Diárias")

# Date selection
selected_date, date_str = selecionar_data()

# Load saved values for this date
existing_row = carregar_queixas_do_dia(date_str)

# Show existing average from saved data
existing_avg = calcular_media_existente(existing_row)
st.metric("Média de sofrimento atual (salvo)", existing_avg)
st.caption("Escala: 0 = sem sofrimento, 10 = sofrimento máximo")
st.divider()

# Render sliders and collect current answers
answers = renderizar_sliders_por_categoria(existing_row, date_str)

# Observation text field
st.divider()
current_obs = str(existing_row.get("observacao", "") or "")
observacao = st.text_area("Observações do dia", value=current_obs, height=120)

# Show session average (before saving)
session_avg = round(sum(answers.values()) / len(answers), 1) if answers else 0.0
st.metric("Média desta sessão", session_avg)

# Save on button click
if st.button("💾 Salvar", type="primary"):
    saved_avg = salvar_queixas(answers, date_str, observacao)
    st.success(f"Queixas salvas! Média do dia: {saved_avg}/10")

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE / "3_queixas")

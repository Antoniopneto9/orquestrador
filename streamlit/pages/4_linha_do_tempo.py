"""Entry point for the Linha do Tempo page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "4_linha_do_tempo" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("4_linha_do_tempo_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
carregar_linha_do_tempo, renderizar_legenda, renderizar_meta_expansivel, salvar_linha_do_tempo = _mod.carregar_linha_do_tempo, _mod.renderizar_legenda, _mod.renderizar_meta_expansivel, _mod.salvar_linha_do_tempo

import streamlit as st


st.set_page_config(page_title="Linha do Tempo", page_icon="🗺", layout="wide")
st.title("🗺 Linha do Tempo")
st.caption("Progresso de cada meta ao longo dos 12 meses da temporada")

# Load data
df = carregar_linha_do_tempo()
if df.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

# Color legend
renderizar_legenda()
st.divider()

# Editable goal cards
st.subheader("Editar Metas")
st.caption("Selecione o status de cada meta por mês e clique em Salvar.")

updated_rows = []
for idx, row in df.iterrows():
    updated_row = renderizar_meta_expansivel(idx, row)
    updated_rows.append(updated_row)

# Save all rows on button click
if st.button("💾 Salvar todas as alterações", type="primary"):
    salvar_linha_do_tempo(updated_rows)
    st.success("Linha do tempo salva com sucesso!")

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE / "4_linha_do_tempo")

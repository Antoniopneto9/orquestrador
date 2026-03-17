"""Entry point for the Linha do Tempo page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import (
    carregar_linha_do_tempo,
    renderizar_legenda,
    renderizar_meta_expansivel,
    salvar_linha_do_tempo,
)

st.set_page_config(page_title="Linha do Tempo", page_icon="🗺", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
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
render_feedback_box(_HERE)

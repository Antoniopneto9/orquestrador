"""Entry point for the Tutor de Dados e IA agent page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[2]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st


st.set_page_config(page_title="Tutor de Dados e IA", page_icon="🤖", layout="wide")
st.title(AGENT_TITLE)
st.caption(AGENT_CAPTION)

st.divider()

filename, content = carregar_ultimo_log()
renderizar_log(filename, content)

st.divider()

listar_todas_sessoes()

"""Entry point for the Coach de Confianca agent page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[2]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from functions import (
    AGENT_TITLE,
    AGENT_CAPTION,
    carregar_ultimo_log,
    renderizar_log,
    listar_todas_sessoes,
)

st.set_page_config(page_title="Coach de Confiança", page_icon="💬", layout="wide")
st.title(AGENT_TITLE)
st.caption(AGENT_CAPTION)

st.divider()

filename, content = carregar_ultimo_log()
renderizar_log(filename, content)

st.divider()

listar_todas_sessoes()

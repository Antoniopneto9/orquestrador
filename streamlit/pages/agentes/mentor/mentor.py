"""Entry point for the Mentor de Rotina agent page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/agentes/mentor/
_STREAMLIT = _HERE.parents[2]                # streamlit/
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

st.set_page_config(page_title="Mentor de Rotina", page_icon="🧭", layout="wide")
st.title(AGENT_TITLE)
st.caption(AGENT_CAPTION)

st.divider()

# Load and display the most recent session log
filename, content = carregar_ultimo_log()
renderizar_log(filename, content)

st.divider()

# List all past sessions
listar_todas_sessoes()

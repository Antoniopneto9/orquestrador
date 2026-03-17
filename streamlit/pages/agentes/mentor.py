"""Entry point for the Mentor de Rotina agent page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/agentes/
_STREAMLIT = _HERE.parents[1]                # streamlit/
_MOD_PATH = _HERE / "mentor" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("mentor_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
AGENT_TITLE, AGENT_CAPTION, carregar_ultimo_log, renderizar_log, listar_todas_sessoes = _mod.AGENT_TITLE, _mod.AGENT_CAPTION, _mod.carregar_ultimo_log, _mod.renderizar_log, _mod.listar_todas_sessoes

import streamlit as st


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

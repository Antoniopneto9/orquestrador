"""Entry point for the Meditacao Joe Dispenza page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "6_meditacao" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("6_meditacao_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
get_steps_data, renderizar_tabela_etapas, renderizar_dicas, renderizar_timer = _mod.get_steps_data, _mod.renderizar_tabela_etapas, _mod.renderizar_dicas, _mod.renderizar_timer

import streamlit as st


st.set_page_config(page_title="Meditação Joe Dispenza", page_icon="🧘", layout="wide")
st.title("🧘 Meditação Joe Dispenza")
st.caption("Protocolo de 25 minutos para reprogramação neurológica")

# Steps reference table
st.subheader("As 5 Etapas")
steps = get_steps_data()
renderizar_tabela_etapas(steps)

st.divider()

# Practical tips
renderizar_dicas()

st.divider()

# Countdown timer
st.subheader("Timer de Sessão")
renderizar_timer()

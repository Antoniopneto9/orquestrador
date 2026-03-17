"""Entry point for the Planejador Financeiro page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # pages/
_STREAMLIT = _HERE.parent                    # streamlit/
_MOD_PATH = _HERE / "9_financeiro" / "functions.py"
sys.path.insert(0, str(_STREAMLIT))

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("9_financeiro_functions", _MOD_PATH)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
tab_lancamentos, tab_dividas, tab_progresso = _mod.tab_lancamentos, _mod.tab_dividas, _mod.tab_progresso

import streamlit as st
from utils.config import SHEET_FINANCEIRO
from utils import xlsx_io

st.set_page_config(page_title="Planejador Financeiro", page_icon="💰", layout="wide")
st.title("💰 Planejador Financeiro")

# Load sheet once and pass to each tab
df = xlsx_io.load_sheet(SHEET_FINANCEIRO)

tab1, tab2, tab3 = st.tabs(["📥 Lançamentos", "🏦 Dívidas", "📈 Progresso"])

with tab1:
    tab_lancamentos(df)

with tab2:
    tab_dividas(df)

with tab3:
    tab_progresso(df)

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE / "9_financeiro")

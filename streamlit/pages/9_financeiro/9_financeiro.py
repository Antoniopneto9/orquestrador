"""Entry point for the Planejador Financeiro page."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import tab_lancamentos, tab_dividas, tab_progresso
from utils.config import SHEET_FINANCEIRO
from utils import xlsx_io

st.set_page_config(page_title="Planejador Financeiro", page_icon="💰", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
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
render_feedback_box(_HERE)

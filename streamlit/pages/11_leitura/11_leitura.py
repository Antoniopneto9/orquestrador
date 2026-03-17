"""Entry point para a página Leitor de Livros."""

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent       # pages/11_leitura/
_STREAMLIT = _HERE.parents[1]                 # streamlit/
sys.path.insert(0, str(_STREAMLIT))
sys.path.insert(0, str(_HERE))

import streamlit as st
from utils.components import render_sidebar_extras, maybe_show_checkin_popup
from functions import carregar_lista_livros, renderizar_leitor

st.set_page_config(page_title="Leitor de Livros", page_icon="📖", layout="wide")
render_sidebar_extras()
maybe_show_checkin_popup()
st.title("📖 Leitor de Livros")

livros = carregar_lista_livros()

if not livros:
    st.warning("Nenhum PDF encontrado. Adicione arquivos `.pdf` em `data/livros/` e recarregue a página.")
    st.stop()

livro_selecionado = st.selectbox("Escolha um livro", livros, key="livro_sel")

renderizar_leitor(livro_selecionado)

from utils.components import render_feedback_box
st.divider()
render_feedback_box(_HERE)

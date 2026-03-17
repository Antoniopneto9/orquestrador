"""
functions.py — Business logic for the Coach de Confianca agent page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import streamlit as st
from utils import xlsx_io

AGENT_NAME = "coach"
AGENT_TITLE = "💬 Coach de Confiança"
AGENT_CAPTION = "Sessões de treino de comunicação assertiva e confronto gradual"


def carregar_ultimo_log() -> tuple:
    """Feature: load the most recent session log file for the coach agent.

    Returns (filename, content) — both empty strings if no log exists.
    """
    return xlsx_io.get_latest_log(AGENT_NAME)


def renderizar_log(filename: str, content: str) -> None:
    """Feature: display the log content with the appropriate renderer.

    Renders markdown as st.markdown, JSON as st.json, and all other formats as plain text.
    """
    if not filename:
        st.info("Nenhuma sessão registrada ainda. Inicie uma sessão no Claude Code.")
        return

    st.subheader("Última Sessão")
    st.caption(f"Arquivo: {filename}")

    if filename.endswith(".md"):
        st.markdown(content)
    elif filename.endswith(".json"):
        import json
        try:
            st.json(json.loads(content))
        except json.JSONDecodeError:
            st.text(content)
    else:
        st.text(content)


def listar_todas_sessoes() -> None:
    """Feature: expander listing all session log files for the coach agent."""
    with st.expander("Todas as sessões"):
        all_logs = xlsx_io.list_agent_logs(AGENT_NAME)

        if not all_logs:
            st.info("Nenhum arquivo de sessão encontrado.")
        else:
            for log_file in all_logs:
                st.markdown(f"- `{log_file}`")

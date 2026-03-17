"""Business logic for the Organização Diária page."""

import sys
import json
from pathlib import Path
from datetime import date

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))

import streamlit as st
from utils.config import SHEET_TAREFAS_DIA
from utils import xlsx_io

HEADERS = ["data", "tarefas_json"]


def carregar_tarefas(date_str: str) -> list:
    """Load the task list for a given date from the Excel sheet."""
    df = xlsx_io.load_sheet(SHEET_TAREFAS_DIA)
    if df.empty or "data" not in df.columns:
        return []
    df["data"] = df["data"].astype(str).str[:10]
    row = df[df["data"] == date_str]
    if row.empty:
        return []
    val = row.iloc[-1]["tarefas_json"]
    try:
        return json.loads(str(val)) if val and str(val) not in ("nan", "") else []
    except Exception:
        return []


def salvar_tarefas(date_str: str, tasks: list) -> None:
    """Persist the task list for the given date, updating if a row already exists."""
    json_str = json.dumps(tasks, ensure_ascii=False)
    df = xlsx_io.load_sheet(SHEET_TAREFAS_DIA)
    if not df.empty and "data" in df.columns:
        df["data"] = df["data"].astype(str).str[:10]
        if date_str in df["data"].values:
            xlsx_io.save_row(SHEET_TAREFAS_DIA, "data", date_str, {"tarefas_json": json_str})
            return
    xlsx_io.append_row(SHEET_TAREFAS_DIA, {"data": date_str, "tarefas_json": json_str}, default_headers=HEADERS)


def renderizar_organizacao_diaria() -> None:
    """Render the daily task manager: add, check off, and delete tasks."""
    today = date.today().strftime("%Y-%m-%d")
    st.markdown(f"### 📋 {today}")

    # Load tasks once per session day
    if "tarefas_dia_loaded" not in st.session_state:
        st.session_state["tarefas_dia_data"] = carregar_tarefas(today)
        st.session_state["tarefas_dia_loaded"] = True

    tasks = st.session_state["tarefas_dia_data"]

    # Input row for adding a new task
    col1, col2 = st.columns([4, 1])
    with col1:
        nova = st.text_input("Nova tarefa", key="nova_tarefa_input", placeholder="Adicionar tarefa...")
    with col2:
        st.write("")
        st.write("")
        if st.button("➕ Adicionar", use_container_width=True):
            if nova.strip():
                tasks.append({"texto": nova.strip(), "concluida": False})
                salvar_tarefas(today, tasks)
                st.session_state["tarefas_dia_data"] = tasks
                st.rerun()

    if not tasks:
        st.info("Nenhuma tarefa para hoje. Adicione uma acima.")
        return

    st.markdown("---")

    # Render each task as a checkbox + delete button pair
    to_remove = None
    for i, t in enumerate(tasks):
        c1, c2 = st.columns([10, 1])
        with c1:
            checked = st.checkbox(
                t["texto"],
                value=t["concluida"],
                key=f"task_check_{i}",
            )
            if checked != t["concluida"]:
                tasks[i]["concluida"] = checked
                salvar_tarefas(today, tasks)
        with c2:
            if st.button("🗑", key=f"del_task_{i}"):
                to_remove = i

    if to_remove is not None:
        tasks.pop(to_remove)
        salvar_tarefas(today, tasks)
        st.session_state["tarefas_dia_data"] = tasks
        st.rerun()

    total = len(tasks)
    done = sum(1 for t in tasks if t["concluida"])
    st.caption(f"{done}/{total} concluídas")

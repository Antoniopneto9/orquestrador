"""
functions.py — Business logic for the Revisao Semanal page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
from datetime import date, timedelta

from utils.config import SEASON_START, SHEET_REVISAO
from utils import xlsx_io


def calcular_semana_atual() -> int:
    """Feature: compute the current week number within the season (1-52)."""
    today = date.today()
    if today < SEASON_START:
        return 1
    days_elapsed = (today - SEASON_START).days
    return min(days_elapsed // 7 + 1, 52)


def carregar_revisao(selected_week: int) -> tuple:
    """Feature: load existing review data for the selected week.

    Returns (df, existing_row) where df is the full sheet and existing_row is a dict.
    """
    df = xlsx_io.load_sheet(SHEET_REVISAO)
    existing_row: dict = {}

    if not df.empty and "semana" in df.columns:
        match = df[df["semana"] == selected_week]
        if not match.empty:
            existing_row = match.iloc[0].to_dict()

    return df, existing_row


def renderizar_formulario(selected_week: int, existing_row: dict) -> tuple:
    """Feature: render the review text areas and score input for the selected week.

    Returns (funcionou, quebrou, ajuste, nota) as strings.
    """
    # Calculate display dates for context
    week_start = SEASON_START + timedelta(weeks=selected_week - 1)
    week_end = week_start + timedelta(days=6)
    st.caption(f"Período: {week_start.strftime('%d/%m/%Y')} a {week_end.strftime('%d/%m/%Y')}")

    st.divider()

    funcionou = st.text_area(
        "O que funcionou esta semana?",
        value=str(existing_row.get("funcionou", "") or ""),
        height=120,
        key=f"funcionou_{selected_week}",
    )
    quebrou = st.text_area(
        "O que quebrei ou não funcionou?",
        value=str(existing_row.get("quebrou", "") or ""),
        height=120,
        key=f"quebrou_{selected_week}",
    )
    ajuste = st.text_area(
        "Ajuste para a próxima semana",
        value=str(existing_row.get("ajuste", "") or ""),
        height=120,
        key=f"ajuste_{selected_week}",
    )

    nota_raw = existing_row.get("nota", "")
    nota = st.text_input(
        "Nota da semana (1-10)",
        value=str(nota_raw) if nota_raw else "",
        key=f"nota_{selected_week}",
    )

    return funcionou, quebrou, ajuste, nota


def salvar_revisao(selected_week: int, funcionou: str, quebrou: str, ajuste: str, nota: str) -> None:
    """Feature: persist the weekly review row to the xlsx sheet."""
    xlsx_io.save_row(
        SHEET_REVISAO,
        "semana",
        selected_week,
        {
            "funcionou": funcionou,
            "quebrou": quebrou,
            "ajuste": ajuste,
            "nota": nota,
        },
    )


def renderizar_historico(df) -> None:
    """Feature: display all past completed reviews inside an expander."""
    with st.expander("Ver todas as revisões anteriores"):
        if df.empty:
            st.info("Nenhuma revisão preenchida ainda.")
            return

        # Show only rows with at least one non-empty review field
        filled = df[
            df[["funcionou", "quebrou", "ajuste", "nota"]]
            .astype(str)
            .apply(lambda row: row.str.strip() != "")
            .any(axis=1)
        ]

        if filled.empty:
            st.info("Nenhuma revisão preenchida ainda.")
            return

        for _, row in filled.sort_values("semana", ascending=False).iterrows():
            week_num = int(row["semana"])
            w_start = SEASON_START + timedelta(weeks=week_num - 1)
            st.markdown(f"**Semana {week_num}** — {w_start.strftime('%d/%m/%Y')}")
            st.markdown(f"- Funcionou: {row.get('funcionou', '')}")
            st.markdown(f"- Quebrou: {row.get('quebrou', '')}")
            st.markdown(f"- Ajuste: {row.get('ajuste', '')}")
            st.markdown(f"- Nota: {row.get('nota', '')}")
            st.divider()

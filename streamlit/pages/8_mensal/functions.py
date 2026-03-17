"""
functions.py — Business logic for the Visao Mensal page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd
from datetime import date

from utils.config import (
    MONTHS_RANGE,
    mensal_sheet_name,
    get_habits_for_date,
)
from utils import xlsx_io

MONTH_LABELS = {
    "2026-03": "Mar/2026", "2026-04": "Abr/2026", "2026-05": "Mai/2026",
    "2026-06": "Jun/2026", "2026-07": "Jul/2026", "2026-08": "Ago/2026",
    "2026-09": "Set/2026", "2026-10": "Out/2026", "2026-11": "Nov/2026",
    "2026-12": "Dez/2026", "2027-01": "Jan/2027", "2027-02": "Fev/2027",
}


def selecionar_mes() -> tuple:
    """Feature: month selectbox defaulting to the current month.

    Returns (selected_key, year, month, sheet_name).
    """
    today = date.today()
    current_month_key = today.strftime("%Y-%m")

    # Default to current month if within season range
    if current_month_key in MONTHS_RANGE:
        default_idx = MONTHS_RANGE.index(current_month_key)
    else:
        default_idx = 0

    selected_key = st.selectbox(
        "Selecione o mês",
        options=MONTHS_RANGE,
        format_func=lambda x: MONTH_LABELS.get(x, x),
        index=default_idx,
    )

    year, month = int(selected_key.split("-")[0]), int(selected_key.split("-")[1])
    sheet = mensal_sheet_name(year, month)

    return selected_key, year, month, sheet


def carregar_mes(sheet_name: str) -> pd.DataFrame:
    """Feature: load the monthly habit sheet and normalize the date column."""
    df = xlsx_io.load_sheet(sheet_name)

    if not df.empty:
        df["data"] = df["data"].astype(str).str[:10]

    return df


def renderizar_cards_resumo(df: pd.DataFrame) -> None:
    """Feature: display filled-days count, percentage metric, and progress bar."""
    total_days = len(df)
    filled_days = int(df["total"].apply(lambda x: x > 0 if pd.notna(x) else False).sum())
    pct_month = round(filled_days / total_days * 100, 1) if total_days > 0 else 0.0

    col1, col2 = st.columns(2)
    col1.metric("Dias preenchidos", f"{filled_days} / {total_days}")
    col2.metric("% do mês preenchido", f"{pct_month}%")

    st.progress(pct_month / 100, text=f"{pct_month}% do mês registrado")


def renderizar_tabela_diaria(df: pd.DataFrame, active_habits: list) -> None:
    """Feature: display the full daily habit table with color-coded S/N cells."""

    def style_sn(val: str) -> str:
        """Return green for S, red for N, empty otherwise."""
        if str(val) == "S":
            return "background-color: #1a7a4a; color: white;"
        elif str(val) == "N":
            return "background-color: #7a1a1a; color: white;"
        return ""

    # Build display column list preserving natural order
    display_cols = ["dia", "data", "dia_semana"] + active_habits + ["total", "percentual"]
    available_cols = [c for c in display_cols if c in df.columns]
    display_df = df[available_cols].copy()

    # Apply S/N coloring only to habit columns
    habit_cols_in_display = [h for h in active_habits if h in display_df.columns]
    styled = display_df.style.applymap(style_sn, subset=habit_cols_in_display)

    st.dataframe(styled, use_container_width=True, hide_index=True)


def renderizar_totais_mes(df: pd.DataFrame, active_habits: list) -> None:
    """Feature: compute and display monthly totals (S count, N count, %) per habit."""
    totals: dict = {}

    for habit in active_habits:
        if habit not in df.columns:
            continue

        col_data = df[habit].astype(str)
        s_count = int((col_data == "S").sum())
        n_count = int((col_data == "N").sum())
        answered = s_count + n_count
        pct = round(s_count / answered * 100, 1) if answered > 0 else 0.0
        totals[habit] = {"S": s_count, "N": n_count, "%": pct}

    if totals:
        totals_df = pd.DataFrame(totals).T.reset_index().rename(columns={"index": "Hábito"})
        st.dataframe(totals_df, use_container_width=True, hide_index=True)

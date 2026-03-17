"""
functions.py — Business logic for the Rastreador Diario page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

# Allow imports from streamlit/ (for utils/)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
from datetime import date

from utils.config import (
    SEASON_START,
    SEASON_END,
    SHEET_RASTREADOR,
    get_habits_for_date,
    get_new_habits_for_date,
)
from utils import xlsx_io

OPTION_LABELS = {"": "⬜ Não preenchido", "S": "✅ Sim", "N": "❌ Não"}
OPTIONS = ["", "S", "N"]


def selecionar_data() -> tuple:
    """Feature: date selector clamped to season range.

    Returns (selected_date, date_str, weekday_name, is_weekend).
    """
    today = date.today()
    # Keep default within season bounds
    default_date = max(SEASON_START, min(today, SEASON_END))

    selected_date = st.date_input(
        "Selecione a data",
        value=default_date,
        min_value=SEASON_START,
        max_value=SEASON_END,
    )

    date_str = selected_date.strftime("%Y-%m-%d")
    weekday_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    weekday_name = weekday_pt[selected_date.weekday()]
    is_weekend = selected_date.weekday() >= 5

    return selected_date, date_str, weekday_name, is_weekend


def carregar_habitos(selected_date: date, date_str: str) -> tuple:
    """Feature: load habits list and existing saved row for the selected date.

    Returns (habits, new_habits, existing_row).
    """
    habits = get_habits_for_date(selected_date)
    new_habits = get_new_habits_for_date(selected_date)
    existing_row = xlsx_io.get_row_by_date(SHEET_RASTREADOR, date_str)
    return habits, new_habits, existing_row


def renderizar_check_in(habits: list, new_habits: list, existing_row: dict, date_str: str) -> dict:
    """Feature: render S/N radio buttons for each habit.

    New habits are marked with a star. Returns answers dict {habit: value}.
    """
    answers: dict = {}

    for habit in habits:
        # Mark habits added this month with a star badge
        is_new = habit in new_habits
        label = f"★ {habit}" if is_new else habit

        # Normalize saved value — default to empty if unrecognized
        current_val = str(existing_row.get(habit, ""))
        if current_val not in OPTIONS:
            current_val = ""
        current_idx = OPTIONS.index(current_val)

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**{label}**")
        with col2:
            answer = st.radio(
                label,
                options=OPTIONS,
                format_func=lambda x: OPTION_LABELS[x],
                index=current_idx,
                key=f"habit_{date_str}_{habit}",
                horizontal=True,
                label_visibility="collapsed",
            )
        answers[habit] = answer

    return answers


def calcular_totais(answers: dict, habits: list) -> tuple:
    """Feature: calculate summary totals from current answers.

    Returns (total_yes, total_habits, pct).
    """
    total_yes = sum(1 for v in answers.values() if v == "S")
    total_habits = len(habits)
    pct = round(total_yes / total_habits * 100, 1) if total_habits > 0 else 0.0
    return total_yes, total_habits, pct


def salvar_check_in(answers: dict, date_str: str, total_yes: int, pct: float) -> None:
    """Feature: save all habit answers and computed totals to the xlsx sheet."""
    # Save each individual habit answer
    for habit, value in answers.items():
        xlsx_io.save_cell(SHEET_RASTREADOR, date_str, habit, value)

    # Save aggregated totals for the day
    xlsx_io.save_cell(SHEET_RASTREADOR, date_str, "total", total_yes)
    xlsx_io.save_cell(SHEET_RASTREADOR, date_str, "percentual", pct)

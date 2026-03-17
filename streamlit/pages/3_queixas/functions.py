"""
functions.py — Business logic for the Queixas Diarias page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
from datetime import date

from utils.config import (
    SEASON_START,
    SEASON_END,
    COMPLAINTS,
    ALL_COMPLAINTS,
    SHEET_QUEIXAS,
)
from utils import xlsx_io


def selecionar_data() -> tuple:
    """Feature: date selector clamped to season range.

    Returns (selected_date, date_str).
    """
    today = date.today()
    default_date = max(SEASON_START, min(today, SEASON_END))

    selected_date = st.date_input(
        "Selecione a data",
        value=default_date,
        min_value=SEASON_START,
        max_value=SEASON_END,
    )
    date_str = selected_date.strftime("%Y-%m-%d")
    return selected_date, date_str


def carregar_queixas_do_dia(date_str: str) -> dict:
    """Feature: load existing queixas row for the selected date from xlsx."""
    return xlsx_io.get_row_by_date(SHEET_QUEIXAS, date_str)


def calcular_media_existente(existing_row: dict) -> float:
    """Feature: compute average suffering score from already-saved values.

    Returns the rounded average (0.0 if no data).
    """
    scores = []
    for complaint in ALL_COMPLAINTS:
        val = existing_row.get(complaint, 0)
        try:
            scores.append(float(val))
        except (TypeError, ValueError):
            scores.append(0.0)

    return round(sum(scores) / len(scores), 1) if scores else 0.0


def renderizar_sliders_por_categoria(existing_row: dict, date_str: str) -> dict:
    """Feature: render 0-10 sliders grouped by category with color feedback.

    Returns answers dict {complaint: score}.
    """
    answers: dict = {}

    for category, complaints in COMPLAINTS.items():
        st.subheader(category)

        for complaint in complaints:
            # Normalize saved value to int, default 0
            current_val = existing_row.get(complaint, 0)
            try:
                current_val = int(float(current_val))
            except (TypeError, ValueError):
                current_val = 0

            score = st.slider(
                complaint,
                min_value=0,
                max_value=10,
                value=current_val,
                key=f"queixa_{date_str}_{complaint}",
            )
            answers[complaint] = score

            # Visual severity feedback
            if score <= 3:
                st.success(f"Nível baixo: {score}/10")
            elif score <= 6:
                st.warning(f"Nível moderado: {score}/10")
            else:
                st.error(f"Nível alto: {score}/10")

    return answers


def salvar_queixas(answers: dict, date_str: str, observacao: str) -> float:
    """Feature: save all slider answers, computed average, and observation to xlsx.

    Returns the session average that was saved.
    """
    session_avg = round(sum(answers.values()) / len(answers), 1) if answers else 0.0

    for complaint, value in answers.items():
        xlsx_io.save_cell(SHEET_QUEIXAS, date_str, complaint, value)

    xlsx_io.save_cell(SHEET_QUEIXAS, date_str, "media", session_avg)
    xlsx_io.save_cell(SHEET_QUEIXAS, date_str, "observacao", observacao)

    return session_avg

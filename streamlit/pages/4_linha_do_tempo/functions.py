"""
functions.py — Business logic for the Linha do Tempo page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd

from utils.config import (
    MONTHS_RANGE,
    GOAL_STATUS_OPTIONS,
    GOAL_STATUS_LABELS,
    GOAL_STATUS_COLORS,
    GOAL_CATEGORIES,
    SHEET_LINHA_TEMPO,
)
from utils import xlsx_io


def carregar_linha_do_tempo() -> pd.DataFrame:
    """Feature: load the goal timeline sheet and ensure all month columns exist."""
    df = xlsx_io.load_sheet(SHEET_LINHA_TEMPO)

    # Add missing month columns so the form always has full coverage
    for m in MONTHS_RANGE:
        if m not in df.columns:
            df[m] = ""

    return df


def renderizar_legenda() -> None:
    """Feature: display color-coded status legend for goal statuses."""
    st.subheader("Legenda")
    legend_cols = st.columns(len(GOAL_STATUS_OPTIONS))

    for col, status in zip(legend_cols, GOAL_STATUS_OPTIONS):
        label = GOAL_STATUS_LABELS.get(status, "—")
        color = GOAL_STATUS_COLORS.get(status, "#f0f0f0")
        col.markdown(
            f'<span style="background-color:{color}; padding:4px 10px; border-radius:4px; color:white;">{label}</span>',
            unsafe_allow_html=True,
        )


def renderizar_meta_expansivel(idx: int, row: pd.Series) -> dict:
    """Feature: render one expandable goal card with month status selectors.

    Returns updated row dict including the sentinel key '_original_meta'.
    """
    meta_name = str(row.get("meta", f"Meta {idx + 1}"))
    categoria = str(row.get("categoria", ""))

    with st.expander(f"{meta_name} — {categoria}", expanded=False):
        col_meta, col_cat = st.columns([2, 2])
        with col_meta:
            new_meta = st.text_input("Nome da meta", value=meta_name, key=f"meta_name_{idx}")
        with col_cat:
            cat_idx = GOAL_CATEGORIES.index(categoria) if categoria in GOAL_CATEGORIES else 0
            new_cat = st.selectbox("Categoria", GOAL_CATEGORIES, index=cat_idx, key=f"cat_{idx}")

        # Month status selectors in grid of 4 per row
        month_values: dict = {}
        month_chunks = [MONTHS_RANGE[i:i + 4] for i in range(0, len(MONTHS_RANGE), 4)]

        for chunk in month_chunks:
            cols = st.columns(len(chunk))
            for col, month in zip(cols, chunk):
                current_status = str(row.get(month, ""))
                if current_status not in GOAL_STATUS_OPTIONS:
                    current_status = ""
                status_idx = GOAL_STATUS_OPTIONS.index(current_status)

                with col:
                    # Color bar above the selectbox as visual indicator
                    color = GOAL_STATUS_COLORS.get(current_status, "#f0f0f0")
                    st.markdown(
                        f'<div style="background:{color}; height:6px; border-radius:3px; margin-bottom:4px;"></div>',
                        unsafe_allow_html=True,
                    )
                    selected = st.selectbox(
                        month,
                        options=GOAL_STATUS_OPTIONS,
                        format_func=lambda x: GOAL_STATUS_LABELS.get(x, "—"),
                        index=status_idx,
                        key=f"status_{idx}_{month}",
                    )
                    month_values[month] = selected

        mes_previsto = str(row.get("mes_previsto", ""))
        observacao = str(row.get("observacao", "") or "")
        new_mes = st.text_input("Mês previsto para conclusão", value=mes_previsto, key=f"mes_{idx}")
        new_obs = st.text_area("Observação", value=observacao, key=f"obs_{idx}", height=80)

    return {
        "meta": new_meta,
        "categoria": new_cat,
        **month_values,
        "mes_previsto": new_mes,
        "observacao": new_obs,
        "_original_meta": meta_name,
    }


def salvar_linha_do_tempo(updated_rows: list) -> None:
    """Feature: persist all updated goal rows to the xlsx sheet."""
    for row_data in updated_rows:
        # Pop the sentinel key before saving — it was only used for lookup
        original_meta = row_data.pop("_original_meta")
        xlsx_io.save_row(SHEET_LINHA_TEMPO, "meta", original_meta, row_data)

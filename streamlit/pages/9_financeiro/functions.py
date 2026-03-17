"""
functions.py — Business logic for the Planejador Financeiro page.

Each function covers one full tab of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd
from datetime import date, timedelta

from utils.config import (
    SEASON_START,
    SEASON_END,
    EXPENSE_CATEGORIES,
    MILLION_GOAL,
    SHEET_FINANCEIRO,
)
from utils import xlsx_io


def tab_lancamentos(df: pd.DataFrame) -> None:
    """Feature: Tab 1 — entry form for income/expenses plus recent entries table."""
    st.subheader("Novo Lançamento")

    today = date.today()
    default_date = max(SEASON_START, min(today, SEASON_END))

    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input(
            "Data",
            value=default_date,
            min_value=SEASON_START,
            max_value=SEASON_END,
            key="fin_date",
        )
        descricao = st.text_input("Descrição", key="fin_desc")
    with col2:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f", key="fin_valor")
        categoria = st.selectbox("Categoria", EXPENSE_CATEGORIES, key="fin_cat")

    if st.button("💾 Salvar lançamento", type="primary"):
        date_str = entry_date.strftime("%Y-%m-%d")
        xlsx_io.save_cell(SHEET_FINANCEIRO, date_str, "descricao", descricao)
        xlsx_io.save_cell(SHEET_FINANCEIRO, date_str, "valor", valor)
        xlsx_io.save_cell(SHEET_FINANCEIRO, date_str, "categoria", categoria)
        st.success(f"Lançamento salvo: {descricao} — R${valor:.2f} ({categoria})")

    st.divider()
    st.subheader("Lançamentos Recentes")

    if df.empty:
        st.info("Nenhum lançamento registrado ainda.")
        return

    # Normalize date and filter to rows with content
    df["data"] = df["data"].astype(str).str[:10]
    recent = df[
        (df["descricao"].astype(str).str.strip() != "") |
        (df["valor"].fillna(0) > 0)
    ].tail(30)

    if recent.empty:
        st.info("Nenhum lançamento registrado ainda.")
    else:
        display_cols = [c for c in ["data", "descricao", "valor", "categoria"] if c in recent.columns]
        st.dataframe(recent[display_cols], use_container_width=True, hide_index=True)


def tab_dividas(df: pd.DataFrame) -> None:
    """Feature: Tab 2 — debt snapshot input and line chart of debt evolution."""
    st.subheader("Registro de Dívida Total")

    today = date.today()
    default_date = max(SEASON_START, min(today, SEASON_END))

    debt_date = st.date_input(
        "Data do registro",
        value=default_date,
        min_value=SEASON_START,
        max_value=SEASON_END,
        key="debt_date",
    )
    debt_value = st.number_input(
        "Dívida total atual (R$)",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="debt_val",
    )

    if st.button("💾 Salvar dívida", key="save_debt"):
        date_str = debt_date.strftime("%Y-%m-%d")
        xlsx_io.save_cell(SHEET_FINANCEIRO, date_str, "divida_total", debt_value)
        st.success(f"Dívida registrada: R${debt_value:,.2f} em {date_str}")

    st.divider()
    st.subheader("Evolução da Dívida")

    if not df.empty and "divida_total" in df.columns:
        df["data"] = df["data"].astype(str).str[:10]
        debt_df = df[df["divida_total"].fillna(0) > 0][["data", "divida_total"]].copy()
        debt_df["divida_total"] = pd.to_numeric(debt_df["divida_total"], errors="coerce").fillna(0)

        if not debt_df.empty:
            st.line_chart(debt_df.set_index("data"))
        else:
            st.info("Nenhum registro de dívida encontrado.")
    else:
        st.info("Nenhum registro de dívida encontrado.")


def tab_progresso(df: pd.DataFrame) -> None:
    """Feature: Tab 3 — patrimônio snapshot, progress bar toward R$1M, and projection."""
    st.subheader("Progresso Rumo ao Primeiro Milhão")

    today = date.today()
    default_date = max(SEASON_START, min(today, SEASON_END))

    pat_date = st.date_input(
        "Data do registro",
        value=default_date,
        min_value=SEASON_START,
        max_value=SEASON_END,
        key="pat_date",
    )
    patrimonio = st.number_input(
        "Patrimônio atual (R$)",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key="patrimonio_val",
    )

    if st.button("💾 Salvar patrimônio", key="save_pat"):
        date_str = pat_date.strftime("%Y-%m-%d")
        xlsx_io.save_cell(SHEET_FINANCEIRO, date_str, "patrimonio", patrimonio)
        st.success(f"Patrimônio registrado: R${patrimonio:,.2f}")

    st.divider()

    # Progress toward the million-real goal
    pct_goal = min(patrimonio / MILLION_GOAL, 1.0)
    st.metric("Meta", f"R${MILLION_GOAL:,.0f}")
    st.metric("Atual", f"R${patrimonio:,.2f}")
    st.progress(pct_goal, text=f"{pct_goal * 100:.2f}% da meta alcançado")

    # Season time context
    days_elapsed = max(0, (today - SEASON_START).days)
    st.metric("Dias decorridos na temporada", days_elapsed)

    # Linear projection: at current daily rate, when will R$1M be reached?
    if patrimonio > 0 and days_elapsed > 0:
        daily_rate = patrimonio / days_elapsed
        days_to_million = MILLION_GOAL / daily_rate
        projected_date = SEASON_START + timedelta(days=int(days_to_million))
        st.metric("Projeção (ritmo atual)", projected_date.strftime("%d/%m/%Y"))
    else:
        st.info("Registre patrimônio em pelo menos 1 data para ver a projeção.")

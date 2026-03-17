"""
functions.py — Business logic for the Correlacao Queixas x Habitos page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import date as date_type

from utils.config import (
    SHEET_RASTREADOR,
    SHEET_QUEIXAS,
    ALL_COMPLAINTS,
    get_habits_for_date,
)
from utils import xlsx_io

MIN_DAYS = 7  # Minimum filled days required before showing the chart


def calcular_pct_habitos_por_dia(df_rastreador: pd.DataFrame) -> pd.DataFrame:
    """Feature: add a pct_habitos column to the rastreador DataFrame.

    Each row gets a % representing how many habits were completed that day.
    """

    def calc_row(row: pd.Series) -> float:
        """Compute habit completion % for one row based on the month's active habits."""
        try:
            d = date_type.fromisoformat(str(row["data"])[:10])
        except (ValueError, TypeError):
            return float("nan")

        habits = get_habits_for_date(d)
        values = [str(row.get(h, "")) for h in habits if h in row.index]
        answered = [v for v in values if v in ("S", "N")]
        yes_count = sum(1 for v in answered if v == "S")
        return round(yes_count / len(habits) * 100, 1) if habits else float("nan")

    df_rastreador["pct_habitos"] = df_rastreador.apply(calc_row, axis=1)
    return df_rastreador


def calcular_media_sofrimento(df_queixas: pd.DataFrame) -> pd.DataFrame:
    """Feature: add a media_sofrimento column to the queixas DataFrame.

    The average is computed across all complaint columns for each day.
    """
    complaint_cols = [c for c in ALL_COMPLAINTS if c in df_queixas.columns]

    df_queixas["media_sofrimento"] = (
        df_queixas[complaint_cols]
        .apply(pd.to_numeric, errors="coerce")
        .mean(axis=1)
    )
    return df_queixas


def mesclar_dados(df_rastreador: pd.DataFrame, df_queixas: pd.DataFrame) -> pd.DataFrame:
    """Feature: inner-join rastreador and queixas on date, keeping only fully filled rows.

    Returns filtered merged DataFrame with only rows where both values are valid.
    """
    merged = pd.merge(
        df_rastreador[["data", "pct_habitos"]],
        df_queixas[["data", "media_sofrimento"]],
        on="data",
        how="inner",
    )

    # Remove rows missing either metric
    merged = merged.dropna(subset=["pct_habitos", "media_sofrimento"])
    merged = merged[merged["pct_habitos"] > 0]

    return merged


def renderizar_grafico_correlacao(merged: pd.DataFrame) -> None:
    """Feature: dual-axis line chart — sofrimento on left (red), habitos% on right (green)."""
    merged_sorted = merged.sort_values("data")
    dates = merged_sorted["data"].tolist()
    pct_habitos = merged_sorted["pct_habitos"].tolist()
    media_sofrimento = merged_sorted["media_sofrimento"].tolist()

    fig, ax1 = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#0e1117")
    ax1.set_facecolor("#0e1117")

    # Left axis: suffering score (red)
    color_sof = "#e8735a"
    ax1.set_xlabel("Data", color="white")
    ax1.set_ylabel("Média de Sofrimento (0-10)", color=color_sof)
    ax1.plot(dates, media_sofrimento, color=color_sof, linewidth=2, label="Sofrimento")
    ax1.tick_params(axis="y", labelcolor=color_sof)
    ax1.tick_params(axis="x", labelcolor="white", rotation=45)
    ax1.set_ylim(0, 10)
    ax1.spines["bottom"].set_color("gray")
    ax1.spines["top"].set_visible(False)
    ax1.spines["left"].set_color(color_sof)
    ax1.spines["right"].set_color("#1a7a4a")

    # Right axis: habit completion % (green dashed)
    ax2 = ax1.twinx()
    color_hab = "#1a7a4a"
    ax2.set_ylabel("% Hábitos Cumpridos", color=color_hab)
    ax2.plot(dates, pct_habitos, color=color_hab, linewidth=2, linestyle="--", label="Hábitos %")
    ax2.tick_params(axis="y", labelcolor=color_hab)
    ax2.set_ylim(0, 100)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", facecolor="#1a1a2e", labelcolor="white")

    # Limit x-axis ticks to avoid crowding
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(12))

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def renderizar_correlacao_completa() -> None:
    """Feature: orchestrate all correlation steps — load, compute, validate, render.

    Handles edge cases: empty data, insufficient days.
    """
    # Load both sheets
    df_rastreador = xlsx_io.load_sheet(SHEET_RASTREADOR)
    df_queixas = xlsx_io.load_sheet(SHEET_QUEIXAS)

    if df_rastreador.empty or df_queixas.empty:
        st.warning("Dados insuficientes. Preencha o Rastreador e as Queixas para ver a correlação.")
        return

    # Normalize date format to YYYY-MM-DD string
    df_rastreador["data"] = df_rastreador["data"].astype(str).str[:10]
    df_queixas["data"] = df_queixas["data"].astype(str).str[:10]

    # Compute derived columns
    df_rastreador = calcular_pct_habitos_por_dia(df_rastreador)
    df_queixas = calcular_media_sofrimento(df_queixas)

    # Merge and filter
    merged = mesclar_dados(df_rastreador, df_queixas)

    if len(merged) < MIN_DAYS:
        st.info(
            f"Preencha pelo menos {MIN_DAYS} dias para ver a correlação. "
            f"Dados disponíveis: {len(merged)} dia(s)."
        )
        return

    # Pearson correlation coefficient
    corr = merged["pct_habitos"].corr(merged["media_sofrimento"])
    st.metric(
        "Correlação (hábitos × sofrimento)",
        f"{corr:.3f}",
        help="Valores negativos indicam que mais hábitos → menos sofrimento.",
    )

    st.subheader("Evolução no Tempo")
    renderizar_grafico_correlacao(merged)

    # Raw data table for inspection
    with st.expander("Ver dados brutos"):
        st.dataframe(merged.sort_values("data").reset_index(drop=True), use_container_width=True)

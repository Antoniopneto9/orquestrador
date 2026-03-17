"""Business logic for the Acontecimentos (events log) page."""

import sys
from pathlib import Path
from datetime import datetime

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))

import streamlit as st
import pandas as pd
from utils.config import SHEET_ACONTECIMENTOS
from utils import xlsx_io

HEADERS = ["data", "hora", "texto"]


def salvar_acontecimento(texto: str) -> None:
    """Append a timestamped event entry to the Excel sheet."""
    agora = datetime.now()
    xlsx_io.append_row(
        SHEET_ACONTECIMENTOS,
        {"data": agora.strftime("%Y-%m-%d"), "hora": agora.strftime("%H:%M"), "texto": texto},
        default_headers=HEADERS,
    )


def carregar_acontecimentos() -> pd.DataFrame:
    """Load and sort all event records, newest first."""
    df = xlsx_io.load_sheet(SHEET_ACONTECIMENTOS)
    if df.empty:
        return df
    if "data" in df.columns and "hora" in df.columns:
        df = df.sort_values(["data", "hora"], ascending=False)
    return df


def renderizar_acontecimentos() -> None:
    """Render the event registration form and the full history table."""
    st.markdown("### ✍️ Registrar acontecimento")
    texto = st.text_area("O que aconteceu?", height=100, placeholder="Anote um evento, pensamento ou situação relevante...")
    if st.button("💾 Salvar", type="primary"):
        if texto.strip():
            salvar_acontecimento(texto.strip())
            st.success("Acontecimento registrado!")
        else:
            st.warning("Escreva algo antes de salvar.")

    st.divider()
    st.markdown("### 📜 Histórico")
    df = carregar_acontecimentos()
    if df.empty:
        st.info("Nenhum acontecimento registrado ainda.")
    else:
        st.dataframe(df, use_container_width=True)

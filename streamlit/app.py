"""
app.py — Welcome page for the Intentional Season 2026 Streamlit app.

Shows season progress, today's date, day number, and a motivational quote.
"""

import streamlit as st
from datetime import date

# Page config must be the first Streamlit call
st.set_page_config(
    page_title="Intentional Season 2026",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import after page config to avoid import-time Streamlit calls
import sys
from pathlib import Path

# Add utils to path so pages can import from it
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import SEASON_START, SEASON_END

# ── Season progress calculation ───────────────────────────────────────────────
today = date.today()
total_days = (SEASON_END - SEASON_START).days + 1

# Clamp today within season bounds for progress display
if today < SEASON_START:
    elapsed = 0
    day_num = 0
elif today > SEASON_END:
    elapsed = total_days
    day_num = total_days
else:
    elapsed = (today - SEASON_START).days + 1
    day_num = elapsed

progress_pct = elapsed / total_days

# ── Motivational quote (from Visualização content) ───────────────────────────
QUOTE = (
    "Você acorda sem odiar o dia. Sem o peso no peito da primeira hora. "
    "O alarme toca e você respira fundo — não por obrigação, mas porque o dia tem sentido."
)

# ── Layout ─────────────────────────────────────────────────────────────────────
st.title("🌱 Intentional Season 2026")
st.caption("Mar/2026 — Mar/2027 · Uma temporada de transformação intencional")

st.divider()

# Season progress bar
st.subheader("Progresso da Temporada")
st.progress(progress_pct, text=f"Dia {day_num} de {total_days} — {progress_pct * 100:.1f}% concluído")

st.divider()

# Info cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Hoje", today.strftime("%d/%m/%Y"))
with col2:
    st.metric("Dia da temporada", f"{day_num} / {total_days}")
with col3:
    days_remaining = total_days - elapsed
    st.metric("Dias restantes", days_remaining)

st.divider()

# Daily quote section
st.subheader("Lembre-se")
st.markdown(
    f"""
    <div style="
        background-color: #1a1a2e;
        border-left: 4px solid #e8735a;
        padding: 1.5rem 1.5rem;
        border-radius: 0 8px 8px 0;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #f0f0f0;
        font-style: italic;
    ">
        "{QUOTE}"
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Navigation hint
st.markdown(
    "Use o menu lateral para navegar entre as seções: "
    "Rastreador, Dashboard, Queixas, Linha do Tempo, Revisão Semanal, e mais."
)

"""Business logic for the Pomodoro / Focus page."""

import sys
from pathlib import Path
from datetime import datetime
import time

_HERE = Path(__file__).resolve().parent
_STREAMLIT = _HERE.parents[1]
sys.path.insert(0, str(_STREAMLIT))

import streamlit as st
import streamlit.components.v1 as components
from utils.config import SHEET_POMODORO
from utils import xlsx_io

POMODORO_HEADERS = ["data", "hora_inicio", "hora_fim", "tipo", "duracao_min", "descricao"]


def inicializar_pomodoro() -> None:
    """Set default Pomodoro session state keys if not yet present."""
    st.session_state.setdefault("pomo_fase", "idle")
    st.session_state.setdefault("pomo_work_min", 25)
    st.session_state.setdefault("pomo_break_min", 5)
    st.session_state.setdefault("pomo_inicio_ts", None)
    st.session_state.setdefault("pomo_descricao", "")
    st.session_state.setdefault("pomo_hora_inicio", "")


def salvar_sessao_pomodoro(tipo: str, duracao_min: float, descricao: str, hora_inicio: str) -> None:
    """Persist a completed Pomodoro session to the Excel sheet."""
    agora = datetime.now()
    xlsx_io.append_row(
        SHEET_POMODORO,
        {
            "data": agora.strftime("%Y-%m-%d"),
            "hora_inicio": hora_inicio,
            "hora_fim": agora.strftime("%H:%M"),
            "tipo": tipo,
            "duracao_min": round(duracao_min, 1),
            "descricao": descricao,
        },
        default_headers=POMODORO_HEADERS,
    )


def renderizar_pomodoro_timer_html(total_seg: int, fase: str) -> None:
    """Render a self-contained JavaScript countdown timer inside an iframe."""
    cor = "#4ade80" if fase == "trabalho" else "#60a5fa"
    label = "🎯 Foco" if fase == "trabalho" else "☕ Pausa"

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #1a1a1a; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 200px; }}
  .container {{ text-align: center; }}
  .label {{ color: #aaa; font-size: 1rem; margin-bottom: 8px; }}
  .timer {{ font-size: 3.5rem; font-weight: bold; color: {cor}; font-variant-numeric: tabular-nums; }}
  .done {{ display: none; color: #fbbf24; font-size: 1.2rem; margin-top: 12px; }}
</style>
</head>
<body>
<div class="container">
  <div class="label">{label}</div>
  <div class="timer" id="t">--:--</div>
  <div class="done" id="done">✅ Sessão concluída!</div>
</div>
<script>
  let remaining = {total_seg};
  const el = document.getElementById('t');
  const done = document.getElementById('done');

  function fmt(s) {{
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return String(m).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
  }}

  el.textContent = fmt(remaining);

  const iv = setInterval(() => {{
    remaining--;
    if (remaining <= 0) {{
      clearInterval(iv);
      el.textContent = '00:00';
      done.style.display = 'block';
    }} else {{
      el.textContent = fmt(remaining);
    }}
  }}, 1000);
</script>
</body>
</html>"""
    components.html(html, height=220)


def renderizar_foco() -> None:
    """Main render function for the Pomodoro page — handles idle, work, and break phases."""
    inicializar_pomodoro()
    fase = st.session_state["pomo_fase"]

    # Idle: configuration form before starting
    if fase == "idle":
        st.markdown("### ⚙️ Configurar sessão")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["pomo_work_min"] = st.number_input(
                "Tempo de foco (min)", min_value=1, max_value=120,
                value=st.session_state["pomo_work_min"], step=1
            )
        with col2:
            st.session_state["pomo_break_min"] = st.number_input(
                "Tempo de pausa (min)", min_value=1, max_value=60,
                value=st.session_state["pomo_break_min"], step=1
            )
        st.session_state["pomo_descricao"] = st.text_input(
            "O que você vai fazer?",
            value=st.session_state["pomo_descricao"],
            placeholder="Ex: Estudar Python, revisar relatório..."
        )

        if st.button("▶ Iniciar foco", type="primary", use_container_width=True):
            st.session_state["pomo_fase"] = "trabalho"
            st.session_state["pomo_inicio_ts"] = time.time()
            st.session_state["pomo_hora_inicio"] = datetime.now().strftime("%H:%M")
            st.rerun()

    # Active work or break phase: show countdown timer and control buttons
    elif fase in ("trabalho", "pausa"):
        total_seg = (
            st.session_state["pomo_work_min"] * 60 if fase == "trabalho"
            else st.session_state["pomo_break_min"] * 60
        )
        inicio_ts = st.session_state.get("pomo_inicio_ts") or time.time()
        elapsed = int(time.time() - inicio_ts)
        remaining = max(0, total_seg - elapsed)

        renderizar_pomodoro_timer_html(remaining, fase)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Concluir sessão", use_container_width=True):
                duracao = elapsed / 60
                salvar_sessao_pomodoro(fase, duracao, st.session_state["pomo_descricao"], st.session_state["pomo_hora_inicio"])
                # Transition: work -> break, break -> idle
                if fase == "trabalho":
                    st.session_state["pomo_fase"] = "pausa"
                    st.session_state["pomo_inicio_ts"] = time.time()
                    st.session_state["pomo_hora_inicio"] = datetime.now().strftime("%H:%M")
                else:
                    st.session_state["pomo_fase"] = "idle"
                st.rerun()
        with col2:
            if st.button("⏹ Cancelar", use_container_width=True):
                st.session_state["pomo_fase"] = "idle"
                st.rerun()

        # Show last 10 sessions for context
        st.divider()
        st.markdown("### 📊 Histórico")
        df = xlsx_io.load_sheet(SHEET_POMODORO)
        if not df.empty:
            st.dataframe(df.tail(10), use_container_width=True)

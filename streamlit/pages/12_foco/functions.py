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
    st.session_state.setdefault("pomo_pausado", False)
    st.session_state.setdefault("pomo_pausa_ts", None)
    st.session_state.setdefault("pomo_elapsed_acumulado", 0)
    # Task list
    st.session_state.setdefault("foco_tarefas", [])
    # Cycle counter
    st.session_state.setdefault("pomo_ciclo", 1)


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


def renderizar_pomodoro_timer_html(total_seg: int, remaining: int, fase: str, pausado: bool) -> None:
    """Render a self-contained JavaScript countdown timer inside an iframe."""
    cor = "#4ade80" if fase == "trabalho" else "#60a5fa"
    label = "Foco" if fase == "trabalho" else "Pausa"
    emoji = "🎯" if fase == "trabalho" else "☕"

    # Progress percentage
    pct = max(0, min(100, int((1 - remaining / max(total_seg, 1)) * 100)))

    # Beep + TTS JS — triggered when remaining hits 0
    fase_proxima = "pausa" if fase == "trabalho" else "trabalho"
    tts_text = f"Hora da {fase_proxima}!" if fase == "trabalho" else "Hora de focar!"

    paused_display = "Pausado" if pausado else ""

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #1a1a1a; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 240px; }}
  .container {{ text-align: center; width: 100%; padding: 0 20px; }}
  .label {{ color: #aaa; font-size: 1rem; margin-bottom: 8px; }}
  .timer {{ font-size: 3.5rem; font-weight: bold; color: {cor}; font-variant-numeric: tabular-nums; }}
  .paused {{ color: #f59e0b; font-size: 0.9rem; margin-top: 6px; height: 1.2em; }}
  .progress-wrap {{ background: #333; border-radius: 8px; height: 12px; margin-top: 16px; overflow: hidden; }}
  .progress-bar {{ height: 100%; background: {cor}; border-radius: 8px; transition: width 1s linear; width: {pct}%; }}
  .done {{ display: none; color: #fbbf24; font-size: 1.2rem; margin-top: 12px; }}
</style>
</head>
<body>
<div class="container">
  <div class="label">{emoji} {label}</div>
  <div class="timer" id="t">--:--</div>
  <div class="paused" id="paused">{paused_display}</div>
  <div class="progress-wrap"><div class="progress-bar" id="pb"></div></div>
  <div class="done" id="done">Sessao concluida!</div>
</div>
<script>
  let remaining = {remaining};
  const total = {total_seg};
  const paused = {'true' if pausado else 'false'};
  const el = document.getElementById('t');
  const pb = document.getElementById('pb');
  const done = document.getElementById('done');

  function fmt(s) {{
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return String(m).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
  }}

  function updatePct(r) {{
    const p = Math.max(0, Math.min(100, Math.round((1 - r / total) * 100)));
    pb.style.width = p + '%';
  }}

  el.textContent = fmt(remaining);
  updatePct(remaining);

  let beeped = false;

  function beepAndSpeak() {{
    if (beeped) return;
    beeped = true;
    // Beep via AudioContext
    try {{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.frequency.value = 880;
      gain.gain.setValueAtTime(0.5, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.0);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 1.0);
    }} catch(e) {{}}
    // TTS
    try {{
      const msg = new SpeechSynthesisUtterance('{tts_text}');
      msg.lang = 'pt-BR';
      window.speechSynthesis.speak(msg);
    }} catch(e) {{}}
  }}

  if (!paused) {{
    const iv = setInterval(() => {{
      remaining--;
      if (remaining <= 0) {{
        clearInterval(iv);
        el.textContent = '00:00';
        pb.style.width = '100%';
        done.style.display = 'block';
        beepAndSpeak();
      }} else {{
        el.textContent = fmt(remaining);
        updatePct(remaining);
      }}
    }}, 1000);
  }} else {{
    el.style.opacity = '0.5';
  }}
</script>
</body>
</html>"""
    components.html(html, height=260)


def renderizar_task_list() -> None:
    """Render task list with add, complete checkbox, notes, and delete for each task."""
    st.markdown("#### Lista de Tarefas")

    tarefas = st.session_state["foco_tarefas"]

    col1, col2 = st.columns([5, 1])
    with col1:
        nova = st.text_input("Nova tarefa", key="nova_foco_tarefa", placeholder="Descreva a tarefa...")
    with col2:
        st.write("")
        st.write("")
        if st.button("Adicionar", key="btn_add_foco_tarefa", use_container_width=True):
            if nova.strip():
                tarefas.append({"texto": nova.strip(), "concluida": False, "anotacao": ""})
                st.session_state["foco_tarefas"] = tarefas
                st.rerun()

    if not tarefas:
        st.caption("Nenhuma tarefa adicionada.")
        return

    total = len(tarefas)
    done = sum(1 for t in tarefas if t["concluida"])
    st.progress(done / total if total else 0, text=f"{done}/{total} concluidas")

    to_remove = None
    for i, t in enumerate(tarefas):
        with st.container():
            c1, c2, c3 = st.columns([1, 8, 1])
            with c1:
                checked = st.checkbox("", value=t["concluida"], key=f"foco_task_chk_{i}", label_visibility="collapsed")
                if checked != t["concluida"]:
                    tarefas[i]["concluida"] = checked
                    st.session_state["foco_tarefas"] = tarefas
                    st.rerun()
            with c2:
                label_style = "~~{}~~".format(t["texto"]) if t["concluida"] else "**{}**".format(t["texto"])
                st.markdown(label_style)
                anotacao = st.text_input(
                    "Anotacao",
                    value=t["anotacao"],
                    key=f"foco_task_nota_{i}",
                    placeholder="Anotacoes sobre esta tarefa...",
                    label_visibility="collapsed",
                )
                if anotacao != t["anotacao"]:
                    tarefas[i]["anotacao"] = anotacao
                    st.session_state["foco_tarefas"] = tarefas
            with c3:
                if st.button("🗑", key=f"foco_task_del_{i}"):
                    to_remove = i

    if to_remove is not None:
        tarefas.pop(to_remove)
        st.session_state["foco_tarefas"] = tarefas
        st.rerun()


def renderizar_foco() -> None:
    """Main render function for the Pomodoro page — handles idle, work, and break phases."""
    inicializar_pomodoro()
    fase = st.session_state["pomo_fase"]
    pausado = st.session_state["pomo_pausado"]

    # --- Task list always visible ---
    renderizar_task_list()
    st.divider()

    st.markdown("### Pomodoro — Ciclo {}".format(st.session_state["pomo_ciclo"]))

    # Idle: configuration form before starting
    if fase == "idle":
        st.markdown("#### Configurar sessao")
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
            "O que voce vai fazer?",
            value=st.session_state["pomo_descricao"],
            placeholder="Ex: Estudar Python, revisar relatorio..."
        )

        if st.button("Iniciar foco", type="primary", use_container_width=True):
            st.session_state["pomo_fase"] = "trabalho"
            st.session_state["pomo_inicio_ts"] = time.time()
            st.session_state["pomo_hora_inicio"] = datetime.now().strftime("%H:%M")
            st.session_state["pomo_pausado"] = False
            st.session_state["pomo_elapsed_acumulado"] = 0
            st.rerun()

    # Active work or break phase: show countdown timer and control buttons
    elif fase in ("trabalho", "pausa"):
        total_seg = (
            st.session_state["pomo_work_min"] * 60 if fase == "trabalho"
            else st.session_state["pomo_break_min"] * 60
        )
        inicio_ts = st.session_state.get("pomo_inicio_ts") or time.time()

        if pausado:
            elapsed = st.session_state["pomo_elapsed_acumulado"]
        else:
            elapsed = st.session_state["pomo_elapsed_acumulado"] + int(time.time() - inicio_ts)

        remaining = max(0, total_seg - elapsed)

        renderizar_pomodoro_timer_html(total_seg, remaining, fase, pausado)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if pausado:
                if st.button("Retomar", use_container_width=True, type="primary"):
                    st.session_state["pomo_pausado"] = False
                    st.session_state["pomo_inicio_ts"] = time.time()
                    st.rerun()
            else:
                if st.button("Pausar", use_container_width=True):
                    st.session_state["pomo_elapsed_acumulado"] = elapsed
                    st.session_state["pomo_pausado"] = True
                    st.rerun()

        with col2:
            if st.button("Concluir sessao", use_container_width=True):
                duracao = elapsed / 60
                salvar_sessao_pomodoro(fase, duracao, st.session_state["pomo_descricao"], st.session_state["pomo_hora_inicio"])
                if fase == "trabalho":
                    st.session_state["pomo_fase"] = "pausa"
                    st.session_state["pomo_inicio_ts"] = time.time()
                    st.session_state["pomo_hora_inicio"] = datetime.now().strftime("%H:%M")
                    st.session_state["pomo_ciclo"] = st.session_state["pomo_ciclo"]
                else:
                    st.session_state["pomo_fase"] = "idle"
                    st.session_state["pomo_ciclo"] += 1
                st.session_state["pomo_pausado"] = False
                st.session_state["pomo_elapsed_acumulado"] = 0
                st.rerun()

        with col3:
            label_skip = "Pular para pausa" if fase == "trabalho" else "Pular para foco"
            if st.button(label_skip, use_container_width=True):
                if fase == "trabalho":
                    st.session_state["pomo_fase"] = "pausa"
                else:
                    st.session_state["pomo_fase"] = "idle"
                    st.session_state["pomo_ciclo"] += 1
                st.session_state["pomo_inicio_ts"] = time.time()
                st.session_state["pomo_hora_inicio"] = datetime.now().strftime("%H:%M")
                st.session_state["pomo_pausado"] = False
                st.session_state["pomo_elapsed_acumulado"] = 0
                st.rerun()

        with col4:
            if st.button("Cancelar", use_container_width=True):
                st.session_state["pomo_fase"] = "idle"
                st.session_state["pomo_pausado"] = False
                st.session_state["pomo_elapsed_acumulado"] = 0
                st.rerun()

        # Show last 10 sessions for context
        st.divider()
        st.markdown("### Historico")
        df = xlsx_io.load_sheet(SHEET_POMODORO)
        if not df.empty:
            st.dataframe(df.tail(10), use_container_width=True)

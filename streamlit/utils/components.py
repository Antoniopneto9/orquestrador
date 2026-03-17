"""Shared UI components rendered across all app pages."""

import sys
from pathlib import Path
import time
from datetime import datetime

_HERE = Path(__file__).resolve().parent      # utils/
_STREAMLIT = _HERE.parent                    # streamlit/
sys.path.insert(0, str(_STREAMLIT))

import streamlit as st
from utils.config import IDEIAS_PATH
from utils import xlsx_io


# ── Check-in dialog ─────────────────────────────────────────────────────────
# Must be defined before maybe_show_checkin_popup references it.

@st.dialog("⚡ Check-in de Energia")
def _show_checkin_dialog() -> None:
    """Inline dialog for periodic energy/focus/mood self-assessment."""
    energia = st.slider("Energia", 1, 5, 3)
    foco = st.slider("Foco", 1, 5, 3)
    humor = st.slider("Humor", 1, 5, 3)
    obs = st.text_input("Observação (opcional)")

    if st.button("Salvar check-in"):
        agora = datetime.now()
        xlsx_io.append_row(
            "checkins",
            {
                "data": agora.strftime("%Y-%m-%d"),
                "hora": agora.strftime("%H:%M"),
                "energia": energia,
                "foco": foco,
                "humor": humor,
                "observacao": obs,
            },
            default_headers=["data", "hora", "energia", "foco", "humor", "observacao"],
        )
        st.session_state["checkin_last_ts"] = time.time()
        st.session_state["checkin_showing"] = False
        st.rerun()


def maybe_show_checkin_popup() -> None:
    """Show energy check-in dialog if 1 hour has passed since the last one."""
    # Initialise timestamp on first call
    if "checkin_last_ts" not in st.session_state:
        st.session_state["checkin_last_ts"] = time.time()
        return

    # Guard: don't call again if already showing
    if st.session_state.get("checkin_showing", False):
        return

    elapsed = time.time() - st.session_state["checkin_last_ts"]
    if elapsed >= 3600:
        st.session_state["checkin_showing"] = True
        _show_checkin_dialog()


# ── Sidebar extras ───────────────────────────────────────────────────────────

def render_sidebar_extras() -> None:
    """Render sidebar widgets: idea capture and optional Pomodoro status."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Ferramentas Rapidas")

        # Ideas capture
        with st.expander("💡 Capturar ideia"):
            idea_text = st.text_area("", key="idea_input_sidebar", height=80, label_visibility="collapsed")
            if st.button("💾 Salvar ideia", key="btn_save_idea_sidebar", use_container_width=True):
                if idea_text.strip():
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    IDEIAS_PATH.parent.mkdir(parents=True, exist_ok=True)
                    with open(IDEIAS_PATH, "a", encoding="utf-8") as f:
                        f.write(f"[{ts}] {idea_text.strip()}\n")
                    st.success("Ideia salva!")

        # Pomodoro status — only shown when a session is active
        fase = st.session_state.get("pomo_fase", "idle")
        if fase != "idle":
            inicio_ts = st.session_state.get("pomo_inicio_ts") or time.time()
            work_min = st.session_state.get("pomo_work_min", 25)
            break_min = st.session_state.get("pomo_break_min", 5)
            total_seg = (work_min if fase == "trabalho" else break_min) * 60
            pausado = st.session_state.get("pomo_pausado", False)
            elapsed_acum = st.session_state.get("pomo_elapsed_acumulado", 0)
            if pausado:
                elapsed = elapsed_acum
            else:
                elapsed = elapsed_acum + int(time.time() - inicio_ts)
            remaining = max(0, total_seg - elapsed)
            mins = remaining // 60
            secs = remaining % 60
            color = "normal" if fase == "trabalho" else "off"
            icon = "🎯" if fase == "trabalho" else "☕"
            pausa_label = " (pausado)" if pausado else ""
            st.markdown("---")
            st.markdown(f"**{icon} Pomodoro ativo**")
            st.metric(
                label=f"{fase.capitalize()}{pausa_label}",
                value=f"{mins:02d}:{secs:02d}",
                delta_color=color,
            )
            ciclo = st.session_state.get("pomo_ciclo", 1)
            st.caption(f"Ciclo {ciclo}")

        st.markdown("---")
        st.caption(f"Sessao iniciada em {datetime.now().strftime('%d/%m/%Y')}")


# ── Per-page feedback box ────────────────────────────────────────────────────

def render_feedback_box(page_folder: Path) -> None:
    """Render a feedback text area that appends submissions to feedback.txt."""
    st.divider()
    st.subheader("💬 Feedback desta página")
    folder_key = page_folder.name
    feedback_text = st.text_area("Seu feedback", key=f"feedback_{folder_key}", label_visibility="collapsed",
                                  placeholder="Deixe um comentário, sugestão ou relato de bug...")
    if st.button("Enviar feedback", key=f"btn_feedback_{folder_key}"):
        if feedback_text.strip():
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            feedback_file = page_folder / "feedback.txt"
            with open(feedback_file, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] PENDENTE: {feedback_text.strip()}\n")
            st.success("Feedback enviado, obrigado!")
        else:
            st.warning("Escreva algo antes de enviar.")

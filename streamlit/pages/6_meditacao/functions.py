"""
functions.py — Business logic for the Meditacao Joe Dispenza page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import streamlit.components.v1 as components
import time


# ── Step data ────────────────────────────────────────────────────────────────
_STEPS = [
    {
        "nome": "1. Reconhecimento e intenção",
        "duracao": "5 min",
        "passo_a_passo": "Sente-se em posição ereta. Feche os olhos. Respire fundo 3x. Declare internamente sua intenção para esta sessão.",
        "onda": "Alfa",
        "neurotransmissores": "Serotonina",
        "objetivo_fisiologico": "Desacelera o cérebro crítico",
        "beneficio_longo_prazo": "Abre estado receptivo",
    },
    {
        "nome": "2. Gratidão antecipada",
        "duracao": "7 min",
        "passo_a_passo": "Sinta gratidão pelo futuro que já existe. Evoque a emoção de ter realizado seus objetivos. Deixe o corpo responder.",
        "onda": "Alfa/Teta",
        "neurotransmissores": "Dopamina, Serotonina",
        "objetivo_fisiologico": "Eleva frequência emocional",
        "beneficio_longo_prazo": "Treina o cérebro para sentir o futuro como real",
    },
    {
        "nome": "3. Visualização da nova identidade",
        "duracao": "8 min",
        "passo_a_passo": "Visualize quem você já é na versão futura. Como anda, fala, se veste, age. Seja aquela pessoa agora.",
        "onda": "Teta",
        "neurotransmissores": "Dopamina, Ocitocina",
        "objetivo_fisiologico": "Ativa circuitos de novas possibilidades",
        "beneficio_longo_prazo": "Reconstrói identidade neurológica",
    },
    {
        "nome": "4. Fusão com o campo",
        "duracao": "5 min",
        "passo_a_passo": "Dissolva os limites do eu. Não há pensamentos, apenas presença. Expanda a consciência além do corpo.",
        "onda": "Teta/Delta",
        "neurotransmissores": "Anandamida, Serotonina",
        "objetivo_fisiologico": "Estado de não-pensamento, conexão total",
        "beneficio_longo_prazo": "Acesso ao estado de criação puro",
    },
    {
        "nome": "5. Gratidão e retorno",
        "duracao": "2 min",
        "passo_a_passo": "Traga a consciência de volta ao corpo. Respire profundamente. Agradeça pelo momento. Abra os olhos devagar.",
        "onda": "Alfa",
        "neurotransmissores": "Endorfina",
        "objetivo_fisiologico": "Ancoragem do estado de paz",
        "beneficio_longo_prazo": "Fecha o ciclo com sensação de completude",
    },
]

TOTAL_SECONDS = 25 * 60  # 25-minute full session


def get_steps_data() -> list:
    """Feature: return the list of meditation step definitions."""
    return _STEPS


def renderizar_tabela_etapas(steps: list) -> None:
    """Feature: display a formatted dataframe with all 5 meditation steps."""
    import pandas as pd

    df = pd.DataFrame(steps).rename(columns={
        "nome": "Etapa",
        "duracao": "Duração",
        "passo_a_passo": "Como fazer",
        "onda": "Onda cerebral",
        "neurotransmissores": "Neurotransmissores",
        "objetivo_fisiologico": "Objetivo fisiológico",
        "beneficio_longo_prazo": "Benefício longo prazo",
    })
    st.dataframe(df, use_container_width=True, hide_index=True)


def renderizar_dicas() -> None:
    """Feature: display 5 practical meditation tips inside an expander."""
    with st.expander("5 Dicas Práticas"):
        st.markdown("""
1. **Ambiente:** Meditação deve ocorrer em silêncio, de preferência no mesmo horário e lugar.
2. **Postura:** Coluna ereta para manter o fluxo de energia. Pode sentar na cadeira com os pés no chão.
3. **Consistência:** 25 dias seguidos criam novos circuitos neurais. Não pule.
4. **Emoção é o sinal:** A emoção é o idioma do corpo. Sem emoção, é só pensamento.
5. **Após a meditação:** Não cheque o celular imediatamente. Permaneça no estado por pelo menos 5 minutos.
""")


def _injetar_beep(frequencia: int = 880, duracao_ms: int = 600) -> None:
    """Feature: play a beep sound in the browser using Web Audio API."""
    components.html(f"""
    <script>
    (function() {{
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime({frequencia}, ctx.currentTime);
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + {duracao_ms / 1000});
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + {duracao_ms / 1000});
    }})();
    </script>
    """, height=0)


def _injetar_tts(texto: str, lang: str = "pt-BR", rate: int = 0) -> None:
    """Feature: speak text in the browser using Web Speech API (SpeechSynthesis).

    rate: relative adjustment (-10 to +10), 0 = default speed.
    """
    # Escape single quotes in text
    texto_safe = texto.replace("'", "\\'")
    components.html(f"""
    <script>
    (function() {{
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{texto_safe}');
        msg.lang = '{lang}';
        msg.rate = 0.9;
        msg.pitch = 1.0;
        msg.volume = 1.0;
        // Pick a Portuguese voice if available
        var voices = window.speechSynthesis.getVoices();
        var ptVoice = voices.find(v => v.lang.startsWith('pt'));
        if (ptVoice) msg.voice = ptVoice;
        window.speechSynthesis.speak(msg);
    }})();
    </script>
    """, height=0)


def _get_step_for_elapsed(elapsed_seconds: int) -> tuple[int, int]:
    """Return (step_index, seconds_elapsed_within_step) for a given total elapsed time."""
    durations = [s["_segundos"] for s in _STEPS]
    acc = 0
    for i, d in enumerate(durations):
        if elapsed_seconds < acc + d:
            return i, elapsed_seconds - acc
        acc += d
    # Beyond total — clamp to last step
    return len(_STEPS) - 1, durations[-1]


def renderizar_timer() -> None:
    """Feature: step-aware meditation timer.

    Shows which step is active, its full context (how-to, brain wave,
    neurotransmitters, objective), a per-step progress bar, and a
    global progress bar. Advances automatically between steps.
    """
    # Attach duration in seconds to each step (mutate module-level list once)
    _durations_sec = [5*60, 7*60, 8*60, 5*60, 2*60]
    for step, dur in zip(_STEPS, _durations_sec):
        step["_segundos"] = dur

    # ── Session state init ────────────────────────────────────────────────────
    for key, val in [("med_running", False), ("med_start", None), ("med_last_step", -1)]:
        if key not in st.session_state:
            st.session_state[key] = val

    st.subheader("▶ Guia de Sessão")

    # ── Controls ──────────────────────────────────────────────────────────────
    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    with col_btn1:
        if not st.session_state.med_running:
            if st.button("▶ Iniciar", type="primary"):
                st.session_state.med_running = True
                st.session_state.med_start = time.time()
                st.session_state.med_last_step = -1
                st.rerun()
    with col_btn2:
        if st.session_state.med_running:
            if st.button("⏹ Parar"):
                st.session_state.med_running = False
                st.session_state.med_start = None
                st.rerun()

    # ── Display ───────────────────────────────────────────────────────────────
    if not st.session_state.med_running or st.session_state.med_start is None:
        st.progress(0.0, text="Pressione ▶ Iniciar para começar")
        return

    elapsed = int(time.time() - st.session_state.med_start)

    if elapsed >= TOTAL_SECONDS:
        st.session_state.med_running = False
        _injetar_beep(frequencia=528, duracao_ms=1500)
        _injetar_tts("Meditação concluída. Permaneça em silêncio por mais cinco minutos.")
        st.balloons()
        st.success("🙏 Meditação concluída! Permaneça em silêncio por mais 5 minutos.")
        return

    step_idx, elapsed_in_step = _get_step_for_elapsed(elapsed)

    # ── Detect step transition — beep + TTS on new step ──────────────────────
    if step_idx != st.session_state.med_last_step:
        st.session_state.med_last_step = step_idx
        step_info = _STEPS[step_idx]
        _injetar_beep(frequencia=660, duracao_ms=400)
        tts_texto = (
            f"Etapa {step_idx + 1}. {step_info['nome'].split('. ', 1)[-1]}. "
            f"Como fazer: {step_info['passo_a_passo']}. "
            f"Onda cerebral: {step_info['onda']}. "
            f"Neurotransmissores ativados: {step_info['neurotransmissores']}. "
            f"Objetivo fisiológico: {step_info['objetivo_fisiologico']}. "
            f"Benefício a longo prazo: {step_info['beneficio_longo_prazo']}."
        )
        _injetar_tts(tts_texto)
    step = _STEPS[step_idx]
    step_dur = step["_segundos"]
    remaining_step = step_dur - elapsed_in_step
    remaining_total = TOTAL_SECONDS - elapsed

    mins_step, secs_step = divmod(remaining_step, 60)
    mins_total, secs_total = divmod(remaining_total, 60)

    # ── Step card ─────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            padding: 1.5rem 2rem;
            border-radius: 12px;
            background-color: #0e1117;
            border-left: 6px solid #e8735a;
            margin-bottom: 1rem;
        ">
            <div style="font-size:1.6rem; font-weight:700; color:#e8735a; margin-bottom:0.5rem;">
                {step['nome']}
            </div>
            <div style="font-size:1.15rem; color:#f0f0f0; margin-bottom:1rem; line-height:1.7;">
                {step['passo_a_passo']}
            </div>
            <div style="display:flex; gap:2rem; flex-wrap:wrap; font-size:0.95rem; color:#aaa;">
                <span>🧠 <b>Onda:</b> {step['onda']}</span>
                <span>⚗️ <b>Neurotransmissores:</b> {step['neurotransmissores']}</span>
                <span>🎯 <b>Objetivo:</b> {step['objetivo_fisiologico']}</span>
                <span>🌱 <b>Benefício:</b> {step['beneficio_longo_prazo']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Step progress bar ─────────────────────────────────────────────────────
    step_pct = min(1.0, elapsed_in_step / step_dur)
    st.progress(step_pct, text=f"Etapa {step_idx + 1}/5 — restam {mins_step:02d}:{secs_step:02d}")

    # ── Step breadcrumb ───────────────────────────────────────────────────────
    breadcrumb = "  →  ".join(
        f"**{s['nome'].split('.')[0]}**" if i == step_idx else s['nome'].split('.')[0]
        for i, s in enumerate(_STEPS)
    )
    st.caption(breadcrumb)

    # ── Global progress bar ───────────────────────────────────────────────────
    global_pct = min(1.0, elapsed / TOTAL_SECONDS)
    st.progress(global_pct, text=f"Sessão total — restam {mins_total:02d}:{secs_total:02d}")

    # Rerun every second to update the timer
    time.sleep(1)
    st.rerun()

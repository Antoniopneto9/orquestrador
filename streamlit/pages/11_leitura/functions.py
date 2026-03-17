"""
functions.py — Features do Leitor de Livros.
Cada função = uma feature da página.
"""

import sys
from pathlib import Path
from datetime import date, datetime
import time
import base64
import random

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import fitz  # pymupdf

from utils.config import LIVROS_PATH, LEITURA_SHEET, LEITURA_COLS
from utils import xlsx_io


# ── Carregar ─────────────────────────────────────────────────────────────────

def carregar_lista_livros() -> list:
    LIVROS_PATH.mkdir(parents=True, exist_ok=True)
    return [p.stem for p in sorted(LIVROS_PATH.glob("*.pdf"))]


def carregar_ultimo_progresso(livro: str) -> int:
    """Lê o último salvamento do Excel e retorna a página_fim. 0 se nenhum."""
    df = xlsx_io.load_sheet(LEITURA_SHEET)
    if df.empty or "livro" not in df.columns:
        return 0
    df_livro = df[df["livro"] == livro]
    if df_livro.empty:
        return 0
    col = "pagina_fim" if "pagina_fim" in df_livro.columns else "pagina"
    try:
        return int(df_livro.iloc[-1][col])
    except Exception:
        return 0


def carregar_total_paginas(livro: str) -> int:
    doc = fitz.open(LIVROS_PATH / f"{livro}.pdf")
    total = doc.page_count
    doc.close()
    return total


@st.cache_data(show_spinner=False)
def carregar_pagina_pdf(livro: str, pagina: int) -> bytes:
    doc = fitz.open(str(LIVROS_PATH / f"{livro}.pdf"))
    page = doc[pagina]
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)
    doc.close()
    return pix.tobytes("png")


def carregar_anotacao_salva(livro: str, pagina: int) -> str:
    """Retorna a última anotação gravada no Excel para livro+página_fim."""
    df = xlsx_io.load_sheet(LEITURA_SHEET)
    if df.empty or "livro" not in df.columns:
        return ""
    col = "pagina_fim" if "pagina_fim" in df.columns else "pagina"
    df_pag = df[(df["livro"] == livro) & (df[col].astype(str) == str(pagina))]
    if df_pag.empty:
        return ""
    val = df_pag.iloc[-1]["anotacao"]
    return str(val) if pd.notna(val) else ""


# ── Rascunhos por página (persistem entre navegações) ─────────────────────────

def inicializar_rascunho(livro: str, pagina: int) -> None:
    key = f"rascunho_{livro}_{pagina}"
    if key not in st.session_state:
        st.session_state[key] = carregar_anotacao_salva(livro, pagina)


def get_rascunho(livro: str, pagina: int) -> str:
    return st.session_state.get(f"rascunho_{livro}_{pagina}", "")


def set_rascunho(livro: str, pagina: int, texto: str) -> None:
    st.session_state[f"rascunho_{livro}_{pagina}"] = texto


# ── Timer (estado em Python, display em JS) ───────────────────────────────────

def inicializar_timer(livro: str) -> None:
    """Inicializa timer parado, sem acumular tempo automaticamente."""
    st.session_state.setdefault(f"timer_rodando_{livro}", False)
    st.session_state.setdefault(f"timer_inicio_{livro}", None)
    st.session_state.setdefault(f"timer_acumulado_{livro}", 0.0)


def get_timer_segundos_iniciais(livro: str) -> int:
    """Calcula segundos totais para passar ao iframe JS como valor inicial."""
    acumulado = st.session_state.get(f"timer_acumulado_{livro}", 0.0)
    rodando = st.session_state.get(f"timer_rodando_{livro}", False)
    inicio = st.session_state.get(f"timer_inicio_{livro}", None)
    if rodando and inicio is not None:
        return int(acumulado + (time.time() - inicio))
    return int(acumulado)


def get_duracao_min(livro: str) -> float:
    return get_timer_segundos_iniciais(livro) / 60


def renderizar_timer_controls(livro: str) -> None:
    """Botões ▶/⏸ e 🔄 — sem st.rerun(), callbacks automáticos."""
    inicializar_timer(livro)
    rodando = st.session_state[f"timer_rodando_{livro}"]

    def _toggle():
        if st.session_state[f"timer_rodando_{livro}"]:
            inicio = st.session_state[f"timer_inicio_{livro}"]
            if inicio:
                st.session_state[f"timer_acumulado_{livro}"] += time.time() - inicio
            st.session_state[f"timer_rodando_{livro}"] = False
            st.session_state[f"timer_inicio_{livro}"] = None
        else:
            st.session_state[f"timer_rodando_{livro}"] = True
            st.session_state[f"timer_inicio_{livro}"] = time.time()

    def _zerar():
        st.session_state[f"timer_rodando_{livro}"] = False
        st.session_state[f"timer_inicio_{livro}"] = None
        st.session_state[f"timer_acumulado_{livro}"] = 0.0

    c1, c2 = st.columns(2)
    with c1:
        label = "⏸ Pausar" if rodando else "▶ Iniciar"
        st.button(label, use_container_width=True, on_click=_toggle, key=f"btn_timer_{livro}")
    with c2:
        st.button("🔄 Zerar", use_container_width=True, on_click=_zerar, key=f"btn_zero_{livro}")


# ── Salvar log estruturado ─────────────────────────────────────────────────────

def salvar_sessao(livro: str, pagina_inicio: int, pagina_fim: int, anotacao: str) -> None:
    """
    Salva uma sessão de leitura com log completo:
    livro, data, hora_inicio, hora_fim, pagina_inicio, pagina_fim,
    paginas_lidas, duracao_min, anotacao.
    """
    agora = datetime.now()
    duracao_min = get_duracao_min(livro)
    hora_inicio_dt = agora.fromtimestamp(
        agora.timestamp() - duracao_min * 60
    )

    xlsx_io.append_row(
        LEITURA_SHEET,
        {
            "livro": livro,
            "data": agora.strftime("%Y-%m-%d"),
            "hora_inicio": hora_inicio_dt.strftime("%H:%M"),
            "hora_fim": agora.strftime("%H:%M"),
            "pagina_inicio": pagina_inicio + 1,
            "pagina_fim": pagina_fim + 1,
            "paginas_lidas": max(0, pagina_fim - pagina_inicio),
            "duracao_min": round(duracao_min, 1),
            "anotacao": anotacao,
        },
        default_headers=LEITURA_COLS,
    )


# ── Renderizar viewer HTML ─────────────────────────────────────────────────────

def renderizar_viewer_html(livro: str, pagina: int, total: int, seg_iniciais: int, rodando: bool) -> None:
    """
    Viewer HTML autossuficiente:
    - Timer corre em JS a partir de seg_iniciais
    - Zoom via slider interno
    - Dica de atalhos na barra superior
    """
    img_bytes = carregar_pagina_pdf(livro, pagina)
    img_b64 = base64.b64encode(img_bytes).decode()
    js_paused = "false" if rodando else "true"

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#1a1a1a; font-family:sans-serif; overflow:hidden; }}
  #reader {{ display:flex; flex-direction:column; height:100vh; width:100%; }}

  #topbar {{
    background:#111; border-bottom:1px solid #333;
    padding:5px 12px; display:flex; align-items:center;
    justify-content:space-between; font-size:0.78rem; color:#666; flex-shrink:0;
  }}
  #timer-display {{
    font-size:1rem; font-weight:bold;
    color: {"#4ade80" if rodando else "#888"};
    font-variant-numeric:tabular-nums;
  }}

  #pdf-area {{
    flex:1; overflow:auto; display:flex;
    justify-content:center; align-items:flex-start;
    background:#2a2a2a; padding:12px;
  }}
  #pdf-img {{ display:block; box-shadow:0 4px 24px rgba(0,0,0,0.6); width:90%; }}

  #bottombar {{
    background:#111; border-top:1px solid #333;
    padding:6px 12px; display:flex; align-items:center;
    gap:8px; flex-shrink:0; flex-wrap:wrap;
  }}
  .nb {{ background:#333; border:none; color:#fff; padding:5px 9px; border-radius:4px; cursor:pointer; font-size:0.95rem; }}
  .nb:hover {{ background:#555; }}
  .nb:disabled {{ opacity:0.3; cursor:default; }}
  #page-info {{ color:#ccc; font-size:0.82rem; }}
  #zoom-val {{ color:#888; font-size:0.78rem; min-width:48px; }}
  input[type=range] {{ width:90px; accent-color:#4a9eff; }}
  #hint {{ color:#444; font-size:0.7rem; margin-left:auto; }}
</style>
</head>
<body>
<div id="reader" tabindex="0">

  <div id="topbar">
    <span>📖 {livro}</span>
    <span id="timer-display">⏱ --:--</span>
    <span>← → navegar &nbsp;|&nbsp; Espaço pausar timer</span>
  </div>

  <div id="pdf-area">
    <img id="pdf-img" src="data:image/png;base64,{img_b64}" />
  </div>

  <div id="bottombar">
    <button class="nb" onclick="nav(0)"           {"disabled" if pagina==0 else ""}>⏮</button>
    <button class="nb" onclick="nav({pagina-1})"  {"disabled" if pagina==0 else ""}>◀</button>
    <span id="page-info">Página <strong>{pagina+1}</strong> de {total}</span>
    <button class="nb" onclick="nav({pagina+1})"  {"disabled" if pagina>=total-1 else ""}>▶</button>
    <button class="nb" onclick="nav({total-1})"   {"disabled" if pagina>=total-1 else ""}>⏭</button>
    <span id="zoom-val">🔍 90%</span>
    <input type="range" id="zs" min="30" max="200" value="90" step="5"
      oninput="document.getElementById('pdf-img').style.width=this.value+'%';
               document.getElementById('zoom-val').textContent='🔍 '+this.value+'%';">
    <span id="hint">← → mudar página</span>
  </div>
</div>

<script>
  // ── Timer em JS — corre em tempo real ─────────────────────────────────────
  let elapsed = {seg_iniciais};
  let paused = {js_paused};
  const display = document.getElementById('timer-display');

  function fmt(s) {{
    const h = Math.floor(s/3600);
    const m = Math.floor((s%3600)/60);
    const sec = s%60;
    if (h>0) return '⏱ '+h+'h '+String(m).padStart(2,'0')+':'+String(sec).padStart(2,'0');
    return '⏱ '+String(m).padStart(2,'0')+':'+String(sec).padStart(2,'0');
  }}

  display.textContent = fmt(elapsed);
  setInterval(() => {{
    if (!paused) {{
      elapsed++;
      display.textContent = fmt(elapsed);
      display.style.color = '#4ade80';
    }}
  }}, 1000);

  // ── Navegação ─────────────────────────────────────────────────────────────
  function nav(page) {{
    window.parent.postMessage({{type:'streamlit:nav', page: page}}, '*');
  }}

  // ── Teclado ───────────────────────────────────────────────────────────────
  document.getElementById('reader').focus();
  document.addEventListener('keydown', (e) => {{
    if (e.key==='ArrowRight') {{ e.preventDefault(); nav({min(pagina+1,total-1)}); }}
    if (e.key==='ArrowLeft')  {{ e.preventDefault(); nav({max(pagina-1,0)}); }}
    if (e.key===' ') {{
      e.preventDefault();
      paused = !paused;
      display.style.color = paused ? '#888' : '#4ade80';
    }}
  }});
</script>
</body>
</html>"""
    components.html(html, height=720, scrolling=False)


# ── Renderizar leitor completo ─────────────────────────────────────────────────

def renderizar_leitor(livro: str) -> None:
    total = carregar_total_paginas(livro)
    key_pag = f"pagina_{livro}"
    key_carregado = f"livro_carregado_{livro}"
    key_pag_inicio = f"pagina_inicio_{livro}"

    # Primeira vez que este livro é aberto na sessão → ler último salvamento do Excel
    if key_carregado not in st.session_state:
        st.session_state[key_pag] = carregar_ultimo_progresso(livro)
        st.session_state[key_pag_inicio] = st.session_state[key_pag]
        st.session_state[key_carregado] = True

    inicializar_timer(livro)

    pagina_atual = st.session_state[key_pag]
    inicializar_rascunho(livro, pagina_atual)
    maybe_show_comprehension_check(livro, pagina_atual)

    seg_iniciais = get_timer_segundos_iniciais(livro)
    rodando = st.session_state[f"timer_rodando_{livro}"]

    col_pdf, col_notas = st.columns([3, 1])

    with col_pdf:
        renderizar_viewer_html(livro, pagina_atual, total, seg_iniciais, rodando)

        # Botões de navegação Streamlit — on_click sem st.rerun()
        def _primeira(): st.session_state[key_pag] = 0
        def _anterior(): st.session_state[key_pag] = max(0, st.session_state[key_pag] - 1)
        def _proxima():  st.session_state[key_pag] = min(total - 1, st.session_state[key_pag] + 1)
        def _ultima():   st.session_state[key_pag] = total - 1

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.button("⏮ Primeira", use_container_width=True, disabled=pagina_atual == 0,        on_click=_primeira)
        with c2: st.button("◀ Anterior", use_container_width=True, disabled=pagina_atual == 0,        on_click=_anterior)
        with c3: st.button("Próxima ▶",  use_container_width=True, disabled=pagina_atual >= total - 1, on_click=_proxima)
        with c4: st.button("Última ⏭",   use_container_width=True, disabled=pagina_atual >= total - 1, on_click=_ultima)

    with col_notas:
        st.markdown("### ⏱ Timer")
        renderizar_timer_controls(livro)

        st.divider()
        st.markdown(f"### 📝 p. {pagina_atual + 1} de {total}")

        def _salvar_rascunho():
            set_rascunho(livro, pagina_atual, st.session_state[f"_ta_{livro}_{pagina_atual}"])

        st.text_area(
            "Notas",
            value=get_rascunho(livro, pagina_atual),
            height=350,
            key=f"_ta_{livro}_{pagina_atual}",
            label_visibility="collapsed",
            placeholder="Anotações desta página...",
            on_change=_salvar_rascunho,
        )

        # Ir para página
        def _ir(): st.session_state[key_pag] = st.session_state[f"_np_{livro}"] - 1
        st.number_input(
            "Ir para página",
            min_value=1, max_value=total,
            value=pagina_atual + 1,
            step=1,
            key=f"_np_{livro}",
            on_change=_ir,
        )

        def _salvar_e_resetar():
            pagina_inicio = st.session_state.get(key_pag_inicio, st.session_state[key_pag])
            pagina_fim = st.session_state[key_pag]
            anotacao = get_rascunho(livro, pagina_fim)
            salvar_sessao(livro, pagina_inicio, pagina_fim, anotacao)
            # Reset for next segment
            st.session_state[key_pag_inicio] = pagina_fim
            st.session_state[f"timer_acumulado_{livro}"] = 0.0
            st.session_state[f"timer_inicio_{livro}"] = None
            st.session_state[f"timer_rodando_{livro}"] = False
            st.session_state[f"sessao_salva_msg_{livro}"] = (pagina_inicio, pagina_fim)

        st.button("💾 Salvar sessão", type="primary", use_container_width=True, on_click=_salvar_e_resetar)
        if f"sessao_salva_msg_{livro}" in st.session_state:
            pi, pf = st.session_state[f"sessao_salva_msg_{livro}"]
            st.success(f"✓ Sessão salva — p.{pi+1}→{pf+1}")

        with st.expander("📋 Histórico de sessões"):
            renderizar_kpis_leitura(livro)
            df = xlsx_io.load_sheet(LEITURA_SHEET)
            if not df.empty and "livro" in df.columns:
                df_livro = df[df["livro"] == livro].copy()
                if not df_livro.empty:
                    cols_show = [c for c in ["data","hora_inicio","hora_fim","pagina_inicio","pagina_fim","paginas_lidas","duracao_min"] if c in df_livro.columns]
                    st.dataframe(df_livro[cols_show].tail(10), use_container_width=True)
                else:
                    st.caption("Nenhuma sessão salva ainda.")


# ── Comprehension check ────────────────────────────────────────────────────────

@st.dialog("🧠 Verificação de Compreensão")
def _show_comp_check(livro: str, pagina_atual: int) -> None:
    """Dialog that asks the user to self-assess understanding of the current page."""
    st.markdown(f"**Página {pagina_atual + 1}** — O que essa página está falando?")
    res = st.radio("Auto-avaliação:", ["✅ Acertei", "❌ Errei"], key=f"comp_radio_{livro}_{pagina_atual}")
    if st.button("Confirmar", key=f"comp_confirm_{livro}"):
        key_showing = f"comp_check_showing_{livro}"
        key_next = f"comp_check_next_{livro}"
        # On failure, rewind two pages; on success, schedule next check further ahead
        if "Errei" in res:
            new_pag = max(0, pagina_atual - 2)
            st.session_state[f"pagina_{livro}"] = new_pag
            st.session_state[key_next] = new_pag + random.randint(3, 7)
        else:
            st.session_state[key_next] = pagina_atual + random.randint(3, 7)
        st.session_state[key_showing] = False
        st.rerun()


def maybe_show_comprehension_check(livro: str, pagina_atual: int) -> None:
    """Trigger a comprehension check dialog once the reader reaches the scheduled page."""
    key_next = f"comp_check_next_{livro}"
    key_showing = f"comp_check_showing_{livro}"

    # Set the first check target on first call for this book
    st.session_state.setdefault(key_next, pagina_atual + random.randint(3, 7))

    # Already showing — do not re-trigger
    if st.session_state.get(key_showing):
        return

    if pagina_atual >= st.session_state[key_next]:
        st.session_state[key_showing] = True
        _show_comp_check(livro, pagina_atual)


# ── Reading KPIs ───────────────────────────────────────────────────────────────

def renderizar_kpis_leitura(livro: str) -> None:
    """Render aggregate reading metrics and a session-duration sparkline."""
    df = xlsx_io.load_sheet(LEITURA_SHEET)
    if df.empty or "livro" not in df.columns:
        return
    df_livro = df[df["livro"] == livro].copy()
    if df_livro.empty:
        return

    total_sessoes = len(df_livro)
    total_anotacoes = df_livro["anotacao"].apply(
        lambda x: bool(str(x).strip()) if pd.notna(x) else False
    ).sum()

    # Compute average minutes per 10 pages when data is available
    if "paginas_lidas" in df_livro.columns and "duracao_min" in df_livro.columns:
        df_valid = df_livro[(df_livro["paginas_lidas"] > 0) & (df_livro["duracao_min"] > 0)]
        avg_min_10 = (df_valid["duracao_min"] / df_valid["paginas_lidas"] * 10).mean() if not df_valid.empty else None
    else:
        avg_min_10 = None

    col1, col2, col3 = st.columns(3)
    col1.metric("Sessões", total_sessoes)
    col2.metric("Com anotações", int(total_anotacoes))
    if avg_min_10 is not None:
        col3.metric("Min/10 pág (média)", f"{avg_min_10:.1f}")

    # Session duration trend line
    if "duracao_min" in df_livro.columns and len(df_livro) > 1:
        st.line_chart(df_livro["duracao_min"].reset_index(drop=True), height=120)

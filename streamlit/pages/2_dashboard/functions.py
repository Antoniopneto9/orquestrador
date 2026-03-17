"""
functions.py — Business logic for the Dashboard de Habitos page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
import pandas as pd

from datetime import date, timedelta
from utils.config import HABITS_BY_MONTH, SHEET_RASTREADOR, SHEET_QUEIXAS, ALL_COMPLAINTS, COMPLAINTS
from utils import xlsx_io


def carregar_dados() -> pd.DataFrame:
    """Feature: load the full rastreador sheet as a DataFrame."""
    return xlsx_io.load_sheet(SHEET_RASTREADOR)


def calcular_metricas_por_habito(df: pd.DataFrame) -> list:
    """Feature: compute cumpridos/falhos/sem_resposta/% for each base habit.

    Returns a list of dicts, one per habit.
    """
    base_habits = HABITS_BY_MONTH["2026-03"]
    metrics = []

    for habit in base_habits:
        if habit not in df.columns:
            continue

        col_data = df[habit].astype(str)
        cumpridos = int((col_data == "S").sum())
        falhos = int((col_data == "N").sum())
        sem_resposta = int((col_data == "").sum() + col_data.isna().sum())
        answered = cumpridos + falhos
        pct = round(cumpridos / answered * 100, 1) if answered > 0 else 0.0

        metrics.append({
            "habito": habit,
            "cumpridos": cumpridos,
            "falhos": falhos,
            "sem_resposta": sem_resposta,
            "percentual": pct,
        })

    return metrics


def renderizar_cards_habitos(metrics: list) -> None:
    """Feature: display metric cards in rows of 4, one card per habit."""
    for row_start in range(0, len(metrics), 4):
        row_habits = metrics[row_start:row_start + 4]
        cols = st.columns(len(row_habits))

        for col, m in zip(cols, row_habits):
            with col:
                st.markdown(f"**{m['habito']}**")
                st.metric("Cumpridos", m["cumpridos"])
                st.metric("Falhos", m["falhos"])
                st.metric("Sem resposta", m["sem_resposta"])
                st.metric("% cumprimento", f"{m['percentual']}%")

        st.divider()


def calcular_total_geral(df: pd.DataFrame) -> tuple:
    """Feature: aggregate totals across all base habits.

    Returns (total_yes, total_no, total_blank, overall_pct).
    """
    base_habits = HABITS_BY_MONTH["2026-03"]

    # Concatenate all habit columns into a single series for aggregation
    all_values = pd.Series(dtype=str)
    for habit in base_habits:
        if habit in df.columns:
            all_values = pd.concat([all_values, df[habit].astype(str)])

    total_yes = int((all_values == "S").sum())
    total_no = int((all_values == "N").sum())
    total_blank = int((all_values == "").sum() + all_values.isna().sum())
    answered = total_yes + total_no
    overall_pct = round(total_yes / answered * 100, 1) if answered > 0 else 0.0

    return total_yes, total_no, total_blank, overall_pct


def carregar_queixas() -> pd.DataFrame:
    """Feature: load full queixas sheet."""
    return xlsx_io.load_sheet(SHEET_QUEIXAS)


def calcular_deltas_queixas(df: pd.DataFrame) -> dict:
    """Feature: compute delta vs d-1, semana-1, mês-1 for media_sofrimento.

    Returns dict with keys: hoje, d1, delta_d1, semana1, delta_semana1, mes1, delta_mes1.
    """
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    d1_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    semana1_str = (today - timedelta(weeks=1)).strftime("%Y-%m-%d")
    mes1_str = (today - timedelta(days=30)).strftime("%Y-%m-%d")

    df = df.copy()
    df["data"] = df["data"].astype(str).str[:10]

    complaint_cols = [c for c in ALL_COMPLAINTS if c in df.columns]

    def media_for_date(d: str) -> float | None:
        row = df[df["data"] == d]
        if row.empty:
            return None
        vals = pd.to_numeric(row.iloc[0][complaint_cols], errors="coerce")
        m = vals.mean()
        return round(float(m), 2) if not pd.isna(m) else None

    hoje = media_for_date(date_str)
    d1 = media_for_date(d1_str)
    semana1 = media_for_date(semana1_str)
    mes1 = media_for_date(mes1_str)

    def delta(atual, ref):
        if atual is None or ref is None:
            return None
        return round(atual - ref, 2)

    return {
        "hoje": hoje,
        "d1": d1, "delta_d1": delta(hoje, d1),
        "semana1": semana1, "delta_semana1": delta(hoje, semana1),
        "mes1": mes1, "delta_mes1": delta(hoje, mes1),
    }


def calcular_evolucao_por_queixa(df: pd.DataFrame) -> pd.DataFrame:
    """Feature: for each complaint, compute mean score and variation vs first 7 days.

    Returns DataFrame sorted by delta ascending (most improved first).
    """
    df = df.copy()
    df["data"] = df["data"].astype(str).str[:10]
    df_sorted = df.sort_values("data")

    complaint_cols = [c for c in ALL_COMPLAINTS if c in df.columns]
    rows = []
    baseline_days = df_sorted.head(7)

    for complaint in complaint_cols:
        col = pd.to_numeric(df_sorted[complaint], errors="coerce")
        baseline = pd.to_numeric(baseline_days[complaint], errors="coerce").mean()
        media_atual = col.mean()
        delta = round(media_atual - baseline, 2) if not pd.isna(baseline) and not pd.isna(media_atual) else None
        rows.append({
            "queixa": complaint,
            "média atual": round(media_atual, 2) if not pd.isna(media_atual) else None,
            "baseline (7d)": round(baseline, 2) if not pd.isna(baseline) else None,
            "variação": delta,
        })

    result = pd.DataFrame(rows).dropna(subset=["variação"])
    return result.sort_values("variação")


def calcular_comparacao_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """Feature: compare average suffering score month vs month.

    Returns DataFrame with columns: mês, média_sofrimento.
    """
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"].astype(str).str[:10], errors="coerce")
    df = df.dropna(subset=["data"])
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    complaint_cols = [c for c in ALL_COMPLAINTS if c in df.columns]
    df[complaint_cols] = df[complaint_cols].apply(pd.to_numeric, errors="coerce")
    df["media_dia"] = df[complaint_cols].mean(axis=1)

    mensal = df.groupby("mes")["media_dia"].mean().reset_index()
    mensal.columns = ["mês", "média_sofrimento"]
    mensal["média_sofrimento"] = mensal["média_sofrimento"].round(2)
    return mensal


def calcular_variacao_media_diaria(df: pd.DataFrame) -> dict:
    """Feature: compute average daily change in suffering score (delta per day).

    Returns dict with: variacao_media_dia, tendencia ('melhora'/'piora'/'estável'), dias_analisados.
    """
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"].astype(str).str[:10], errors="coerce")
    complaint_cols = [c for c in ALL_COMPLAINTS if c in df.columns]
    df[complaint_cols] = df[complaint_cols].apply(pd.to_numeric, errors="coerce")
    df["media_dia"] = df[complaint_cols].mean(axis=1)

    serie = df[df["media_dia"] > 0][["data", "media_dia"]].dropna().sort_values("data").reset_index(drop=True)

    if len(serie) < 2:
        return {"variacao_media_dia": None, "tendencia": None, "dias_analisados": len(serie)}

    deltas = serie["media_dia"].diff().dropna()
    variacao_media = round(deltas.mean(), 3)

    if variacao_media < -0.05:
        tendencia = "melhora"
    elif variacao_media > 0.05:
        tendencia = "piora"
    else:
        tendencia = "estável"

    return {
        "variacao_media_dia": variacao_media,
        "tendencia": tendencia,
        "dias_analisados": len(serie),
    }


def renderizar_filtros_queixas(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Feature: sidebar filters for complaints section.

    Filters: date range, categories (multiselect), individual complaints (multiselect).
    Returns (df_filtered, selected_complaints).
    """
    from utils.config import SEASON_START, SEASON_END

    st.sidebar.header("🔍 Filtros — Queixas")

    # ── Date range ────────────────────────────────────────────────────────────
    df_raw = df_raw.copy()
    df_raw["data"] = pd.to_datetime(df_raw["data"].astype(str).str[:10], errors="coerce")
    datas_validas = df_raw["data"].dropna()

    min_data = datas_validas.min().date() if not datas_validas.empty else SEASON_START
    max_data = datas_validas.max().date() if not datas_validas.empty else SEASON_END

    date_range = st.sidebar.date_input(
        "Período",
        value=(min_data, max_data),
        min_value=SEASON_START,
        max_value=SEASON_END,
        key="filtro_periodo",
    )

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
    else:
        start, end = min_data, max_data

    df_filtrado = df_raw[
        (df_raw["data"].dt.date >= start) &
        (df_raw["data"].dt.date <= end)
    ].copy()

    # ── Category filter ───────────────────────────────────────────────────────
    categorias_disponiveis = list(COMPLAINTS.keys())
    categorias_sel = st.sidebar.multiselect(
        "Categorias",
        options=categorias_disponiveis,
        default=categorias_disponiveis,
        key="filtro_categorias",
    )

    # Build complaint list from selected categories
    queixas_da_categoria = [
        q for cat in categorias_sel
        for q in COMPLAINTS.get(cat, [])
        if q in df_filtrado.columns
    ]

    # ── Individual complaint filter ───────────────────────────────────────────
    queixas_sel = st.sidebar.multiselect(
        "Queixas específicas",
        options=queixas_da_categoria,
        default=queixas_da_categoria,
        key="filtro_queixas",
    )

    # ── Dias com preenchimento mínimo ─────────────────────────────────────────
    min_score = st.sidebar.slider(
        "Score mínimo de qualquer queixa no dia",
        min_value=0, max_value=10, value=0,
        help="Filtra dias onde pelo menos uma queixa atingiu esse valor",
        key="filtro_min_score",
    )

    if min_score > 0 and queixas_sel:
        mask = df_filtrado[queixas_sel].apply(pd.to_numeric, errors="coerce").max(axis=1) >= min_score
        df_filtrado = df_filtrado[mask]

    st.sidebar.caption(f"📅 {len(df_filtrado)} dias no período | {len(queixas_sel)} queixas selecionadas")

    return df_filtrado, queixas_sel


def renderizar_kpis_queixas(df: pd.DataFrame) -> None:
    """Feature: render all complaint KPIs — filters, deltas, evolution ranking, monthly comparison."""

    st.subheader("📉 Evolução das Queixas")

    # Apply sidebar filters first
    df_filtrado, queixas_sel = renderizar_filtros_queixas(df)

    # Use filtered complaints for all subsequent calculations
    df_calc = df_filtrado.copy()
    if queixas_sel:
        cols_keep = ["data"] + [c for c in queixas_sel if c in df_calc.columns]
        df_calc = df_calc[cols_keep]

    if df_calc.empty or len(df_calc) < 2:
        st.info("Preencha pelo menos 2 dias de queixas (ou ajuste os filtros) para ver a evolução.")
        return

    # ── Deltas d-1, semana-1, mês-1 (sempre sobre df original para contexto) ──
    deltas = calcular_deltas_queixas(df)
    hoje = deltas["hoje"]

    st.markdown("**Média de sofrimento — variações**")
    col1, col2, col3, col4 = st.columns(4)

    def fmt_delta(d):
        if d is None:
            return None
        return f"{'+' if d > 0 else ''}{d}"

    col1.metric("Hoje", f"{hoje:.2f}" if hoje is not None else "—")
    col2.metric("vs Ontem (d-1)", f"{deltas['d1']:.2f}" if deltas['d1'] is not None else "—",
                delta=fmt_delta(deltas["delta_d1"]), delta_color="inverse")
    col3.metric("vs Semana passada", f"{deltas['semana1']:.2f}" if deltas['semana1'] is not None else "—",
                delta=fmt_delta(deltas["delta_semana1"]), delta_color="inverse")
    col4.metric("vs Mês passado", f"{deltas['mes1']:.2f}" if deltas['mes1'] is not None else "—",
                delta=fmt_delta(deltas["delta_mes1"]), delta_color="inverse")

    st.caption("🟢 Delta negativo = melhora (menos sofrimento) | 🔴 Delta positivo = piora")

    # ── Variação média diária (sobre período filtrado) ────────────────────────
    var = calcular_variacao_media_diaria(df_calc)
    if var["variacao_media_dia"] is not None:
        v = var["variacao_media_dia"]
        tendencia = var["tendencia"]
        emoji = "🟢" if tendencia == "melhora" else ("🔴" if tendencia == "piora" else "🟡")
        st.metric(
            f"{emoji} Variação média por dia — período filtrado ({var['dias_analisados']} dias)",
            f"{'+' if v > 0 else ''}{v:.3f} pts/dia",
            help="Média de quanto a pontuação de sofrimento sobe ou desce a cada dia no período selecionado.",
        )

    st.divider()

    # ── Ranking por queixa (filtrado) ─────────────────────────────────────────
    evolucao = calcular_evolucao_por_queixa(df_calc)

    if not evolucao.empty:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**🏆 Queixas que mais melhoraram**")
            top_melhoras = evolucao[evolucao["variação"] < 0].head(5)
            if top_melhoras.empty:
                st.info("Nenhuma melhora registrada ainda.")
            else:
                for _, row in top_melhoras.iterrows():
                    st.metric(row["queixa"][:35], f"{row['média atual']:.1f}/10",
                              delta=f"{row['variação']:.2f}", delta_color="inverse")

        with col_b:
            st.markdown("**⚠️ Queixas que mais pioraram**")
            top_pioras = evolucao[evolucao["variação"] > 0].sort_values("variação", ascending=False).head(5)
            if top_pioras.empty:
                st.info("Nenhuma piora registrada.")
            else:
                for _, row in top_pioras.iterrows():
                    st.metric(row["queixa"][:35], f"{row['média atual']:.1f}/10",
                              delta=f"+{row['variação']:.2f}", delta_color="inverse")

        st.divider()

        with st.expander("Ver variação completa por queixa"):
            st.dataframe(evolucao.reset_index(drop=True), use_container_width=True, hide_index=True)

    # ── Comparação mês a mês ──────────────────────────────────────────────────
    mensal = calcular_comparacao_mensal(df_calc)
    if len(mensal) >= 2:
        st.markdown("**📅 Comparação mês a mês — média de sofrimento**")
        st.bar_chart(mensal.set_index("mês")[["média_sofrimento"]])
    elif len(mensal) == 1:
        st.info("Dados de apenas 1 mês — comparação disponível a partir do 2º mês.")

    # ── Evolução diária (série temporal, filtrada) ────────────────────────────
    df2 = df_calc.copy()
    df2["data"] = pd.to_datetime(df2["data"].astype(str).str[:10], errors="coerce")
    complaint_cols = [c for c in queixas_sel if c in df2.columns]
    if complaint_cols:
        df2[complaint_cols] = df2[complaint_cols].apply(pd.to_numeric, errors="coerce")
        df2["media_dia"] = df2[complaint_cols].mean(axis=1)
        serie = df2[df2["media_dia"] > 0][["data", "media_dia"]].dropna().sort_values("data")
        if len(serie) >= 2:
            st.markdown("**📈 Evolução diária da média de sofrimento**")
            st.line_chart(serie.set_index("data")[["media_dia"]])


def renderizar_grafico(metrics: list) -> None:
    """Feature: render a bar chart showing % completion per habit."""
    if not metrics:
        return

    chart_df = pd.DataFrame(metrics).set_index("habito")[["percentual"]]
    # Truncate long habit names so the chart stays readable
    chart_df.index = [h[:20] + "…" if len(h) > 20 else h for h in chart_df.index]
    st.bar_chart(chart_df)

from pathlib import Path
import calendar

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[2]  # project root (intentional_season/)
XLSX_PATH = BASE_DIR / "data" / "intentional_season.xlsx"
LOGS_BASE_PATH = BASE_DIR / "logs" / "sessoes"
LIVROS_PATH    = BASE_DIR / "data" / "livros"

# ── Leitura ─────────────────────────────────────────────────────────────────
LEITURA_SHEET = "leitura"
LEITURA_COLS  = ["livro", "data", "hora_inicio", "hora_fim", "pagina_inicio", "pagina_fim", "paginas_lidas", "duracao_min", "anotacao"]

# ── Habits ─────────────────────────────────────────────────────────────────────
HABITS_BY_MONTH = {
    "2026-03": [
        "Meditação 25min", "Sem Ritalina após 14h", "Dormir antes 00h",
        "Sem pornô", "Instagram <10min", "Treino", "Sem álcool", "Leitura 10 páginas",
    ],
    "2026-04": [
        "Meditação 25min", "Sem Ritalina após 14h", "Dormir antes 00h",
        "Sem pornô", "Instagram <10min", "Treino", "Sem álcool", "Leitura 10 páginas",
        "Banho frio", "Skincare diário", "Contato semanal com gestor",
    ],
    "2026-05": [
        "Meditação 25min", "Sem Ritalina após 14h", "Dormir antes 00h",
        "Sem pornô", "Instagram <10min", "Treino", "Sem álcool", "Leitura 10 páginas",
        "Banho frio", "Skincare diário", "Contato semanal com gestor",
        "Estudo 3h fim de semana", "Preparar 1 ponto por reunião",
    ],
    "2026-06": [
        "Meditação 25min", "Sem Ritalina após 14h", "Dormir antes 00h",
        "Sem pornô", "Instagram <10min", "Treino", "Sem álcool", "Leitura 10 páginas",
        "Banho frio", "Skincare diário", "Contato semanal com gestor",
        "Estudo 3h fim de semana", "Preparar 1 ponto por reunião",
        "Gravar áudio treino de voz", "Reunião feedback com líder",
    ],
    "2026-07": [
        "Meditação 25min", "Sem Ritalina após 14h", "Dormir antes 00h",
        "Sem pornô", "Instagram <10min", "Treino", "Sem álcool", "Leitura 10 páginas",
        "Banho frio", "Skincare diário", "Contato semanal com gestor",
        "Estudo 3h fim de semana", "Preparar 1 ponto por reunião",
        "Gravar áudio treino de voz", "Reunião feedback com líder",
        "Propor melhoria no trabalho", "Projeto de renda extra",
    ],
    "2026-08": [
        "Meditação 25min", "Sem Ritalina após 14h", "Dormir antes 00h",
        "Sem pornô", "Instagram <10min", "Treino", "Sem álcool", "Leitura 10 páginas",
        "Banho frio", "Skincare diário", "Contato semanal com gestor",
        "Estudo 3h fim de semana", "Preparar 1 ponto por reunião",
        "Gravar áudio treino de voz", "Reunião feedback com líder",
        "Propor melhoria no trabalho", "Projeto de renda extra",
        "Controle financeiro", "Leitura de retórica",
    ],
    # Sep 2026 – Feb 2027: same as August (no new habits defined yet)
    "2026-09": None,  # filled below
    "2026-10": None,
    "2026-11": None,
    "2026-12": None,
    "2027-01": None,
    "2027-02": None,
}

# Fill remaining months with August list
_aug = HABITS_BY_MONTH["2026-08"]
for _m in ["2026-09","2026-10","2026-11","2026-12","2027-01","2027-02"]:
    HABITS_BY_MONTH[_m] = _aug[:]

NEW_HABITS: dict[str, list[str]] = {
    "2026-04": ["Banho frio", "Skincare diário", "Contato semanal com gestor"],
    "2026-05": ["Estudo 3h fim de semana", "Preparar 1 ponto por reunião"],
    "2026-06": ["Gravar áudio treino de voz", "Reunião feedback com líder"],
    "2026-07": ["Propor melhoria no trabalho", "Projeto de renda extra"],
    "2026-08": ["Controle financeiro", "Leitura de retórica"],
}

def get_habits_for_date(date_obj) -> list[str]:
    key = date_obj.strftime("%Y-%m")
    for month in sorted(HABITS_BY_MONTH.keys(), reverse=True):
        if key >= month:
            return HABITS_BY_MONTH[month]
    return HABITS_BY_MONTH["2026-03"]

def get_new_habits_for_date(date_obj) -> list[str]:
    key = date_obj.strftime("%Y-%m")
    return NEW_HABITS.get(key, [])

# ── Complaints ─────────────────────────────────────────────────────────────────
COMPLAINTS: dict[str, list[str]] = {
    "Mente e Emoções": [
        "Esgotamento mental", "Ansiedade constante", "Tristeza e falta de brilho",
        "Não acredita na própria visão", "Planeja mas não executa", "Autodesvalorização",
    ],
    "Confiança e Comunicação": [
        "Falta de confiança", "Medo de se expressar", "Trava ao argumentar sob pressão",
        "Evitação de conflitos", "Invisível para gestores", "Não consegue dizer não",
        "Não fala primeiro",
    ],
    "Sono e Rotina": ["Insônia", "Manhã infernal", "Home office sem estrutura"],
    "Escapismo e Hábitos": [
        "Pornografia", "Instagram compulsivo", "Séries e YouTube sem controle",
        "Comida por ansiedade",
    ],
    "Imagem e Corpo": ["Insatisfação com a própria imagem"],
    "Carreira e Finanças": [
        "Medo de ser cortado", "Não progride na carreira",
        "Dívidas de consumo", "Distância do primeiro milhão",
    ],
}

ALL_COMPLAINTS: list[str] = [c for cats in COMPLAINTS.values() for c in cats]

# ── Goal statuses ───────────────────────────────────────────────────────────────
GOAL_STATUS_OPTIONS = ["", "starts", "in_progress", "consolidated", "done"]
GOAL_STATUS_LABELS = {
    "": "—",
    "starts": "🟢 Inicia",
    "in_progress": "🟡 Em andamento",
    "consolidated": "🟣 Consolidado",
    "done": "🪸 Concluído",
}
GOAL_STATUS_COLORS: dict[str, str] = {
    "starts":       "#1a7a4a",
    "in_progress":  "#e6b800",
    "consolidated": "#6a0dad",
    "done":         "#e8735a",
    "":             "#f0f0f0",
}

GOAL_CATEGORIES = [
    "Pilares Inegociáveis",
    "Rotina Matinal",
    "Estudo e Carreira",
    "Confiança e Comunicação",
    "Aparência e Autocuidado",
    "Financeiro e Vida Material",
    "Bem-estar e Saúde Mental",
]

MONTHS_RANGE = [
    "2026-03","2026-04","2026-05","2026-06","2026-07","2026-08",
    "2026-09","2026-10","2026-11","2026-12","2027-01","2027-02",
]

# ── Financial ──────────────────────────────────────────────────────────────────
MILLION_GOAL = 1_000_000.00
EXPENSE_CATEGORIES = [
    "Alimentação", "Transporte", "Moradia", "Saúde", "Educação",
    "Lazer", "Roupas", "Dívidas", "Outros",
]

# ── Sheet names ────────────────────────────────────────────────────────────────
SHEET_RASTREADOR  = "rastreador"
SHEET_QUEIXAS     = "queixas"
SHEET_REVISAO     = "revisao_semanal"
SHEET_LINHA_TEMPO = "linha_do_tempo"
SHEET_DASHBOARD   = "dashboard"
SHEET_FINANCEIRO  = "financeiro"
SHEET_CHECKINS       = "checkins"
SHEET_POMODORO       = "pomodoro"
SHEET_TAREFAS_DIA    = "tarefas_dia"
SHEET_ACONTECIMENTOS = "acontecimentos"
IDEIAS_PATH          = BASE_DIR / "data" / "ideias.txt"

def mensal_sheet_name(year: int, month: int) -> str:
    abbr = calendar.month_abbr[month].lower()
    return f"mensal_{abbr}{year}"

MENSAL_SHEETS = [mensal_sheet_name(2026, m) for m in range(3, 13)] + \
                [mensal_sheet_name(2027, m) for m in range(1, 3)]

# ── Season dates ───────────────────────────────────────────────────────────────
from datetime import date
SEASON_START = date(2026, 3, 16)
SEASON_END   = date(2027, 3, 15)

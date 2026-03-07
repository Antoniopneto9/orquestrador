from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PROJECT_PRESENTATION.md"


DESCRIPTIONS = {
    ".gitignore": "Ignora arquivos temporarios e de ambiente no Git.",
    "README.md": "Resumo executivo do projeto e fluxo principal.",
    "PROJECT_RULES.md": "Fonte normativa de governanca operacional (MUST/MUST NOT).",
    "PROJECT_PRESENTATION.md": "Guia visual e funcional para estudo da base.",
    "CLAUDE.md": "Bootstrap obrigatorio e regras para sessoes de IA.",
    "CONTRIBUTING.md": "Como contribuir sem quebrar os padroes da base.",
    "CHANGELOG.md": "Historico de versoes e mudancas.",
    "SECURITY.md": "Politica de seguranca e reporte de vulnerabilidades.",
    "LICENSE": "Licenca legal de uso.",
    ".claude/agents/README.md": "Catalogo dos agentes disponiveis.",
    ".claude/agents/_template.md": "Template para criar novo agente.",
    ".claude/commands/README.md": "Catalogo dos comandos slash.",
    ".claude/kb/README.md": "Como usar e manter a base de conhecimento.",
    ".claude/kb/_index.yaml": "Indice dos dominios KB.",
    ".claude/sdd/README.md": "Guia da camada SDD.",
    ".claude/sdd/_index.md": "Mapa resumido da camada SDD.",
    ".claude/sdd/architecture/ARCHITECTURE.md": "Visao arquitetural do metodo.",
    ".claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml": "Contrato de fases, gates e padroes.",
    ".claude/project-memory/README.md": "Guia da camada de memoria operacional.",
    ".claude/project-memory/project-manifest.md": "Objetivo, guardrails e direcao do projeto.",
    ".claude/project-memory/current-state.md": "Foto atual para retomar trabalho rapido.",
    ".claude/project-memory/roadmap.json": "Plano por areas com status e dependencias.",
    ".claude/project-memory/metrics/progress-snapshot.json": "Snapshot de progresso global e por area.",
    ".claude/project-memory/metrics/weekly-metrics.json": "Metricas e previsao semanal.",
    ".claude/project-memory/reports/executive-status.md": "Resumo executivo para decisores.",
    "docs/README.md": "Entrada da documentacao.",
    "docs/getting-started/README.md": "Passo a passo para comecar.",
    "docs/concepts/README.md": "Conceitos e modelo mental.",
    "docs/reference/README.md": "Referencia de comandos/agentes/templates.",
    "docs/tutorials/README.md": "Tutoriais de uso.",
}


def list_files() -> list[str]:
    files = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or rel.startswith(".sandbox/"):
            continue
        files.append(rel)
    return sorted(files)


def tree_lines() -> list[str]:
    lines = []
    top = sorted([p for p in ROOT.iterdir() if p.name not in {".git", ".sandbox"}], key=lambda x: x.name.lower())
    for i, item in enumerate(top):
        elbow = "`-- " if i == len(top) - 1 else "|-- "
        lines.append(f"{elbow}{item.name}")
        if item.is_dir() and item.name in {".claude", "docs", "scripts"}:
            children = sorted([c for c in item.iterdir()], key=lambda x: x.name.lower())
            for j, child in enumerate(children):
                branch = "    `-- " if j == len(children) - 1 else "    |-- "
                lines.append(f"{branch}{child.name}")
    return lines


def classify(rel: str) -> str:
    if rel in DESCRIPTIONS:
        return DESCRIPTIONS[rel]
    if rel.startswith(".claude/agents/"):
        return "Definicao de agente especializado (papel, gatilhos, processo, quality gate)."
    if rel.startswith(".claude/commands/"):
        return "Definicao de comando operacional em markdown."
    if rel.startswith(".claude/sdd/templates/"):
        return "Template de artefato da fase SDD."
    if rel.startswith(".claude/kb/_templates/"):
        return "Template de dominio da base de conhecimento."
    if rel.startswith(".claude/project-memory/templates/"):
        return "Template da camada de memoria operacional."
    if rel.endswith(".gitkeep"):
        return "Placeholder para manter pasta versionada."
    return "Arquivo de suporte do framework."


def build_md(files: list[str]) -> str:
    tree = "\n".join(tree_lines())
    rows = "\n".join(f"| `{f}` | {classify(f)} |" for f in files)
    return f"""# PROJECT PRESENTATION

Guia visual, funcional e didatico da base para estudo e decisao de uso.

## 1) Fluxo Q (como o sistema funciona)

Q = Pergunta/Ideia -> Especificacao -> Execucao -> Memoria -> Proxima acao

```text
+--------------------------------------------------------------------------------+
|                                  FLUXO Q                                       |
+--------------------------------------------------------------------------------+
| Ideia                                                                          |
|   |                                                                            |
|   +--> /brainstorm --> /define --> /design                                     |
|                                     |                                          |
|                                     +--> /start-project                        |
|                                           |                                    |
|                                           +--> /build                          |
|                                                 |                              |
|                                                 +--> /checkpoint               |
|                                                        |                       |
|                                                        +--> /status            |
|                                                        +--> /forecast-week     |
|                                                                   |            |
|                                                                   +--> /ship   |
+--------------------------------------------------------------------------------+
```

## 2) Dependencias (quem chama quem)

```text
+--------------------+      +--------------------+      +---------------------+
| commands/*.md      | ---> | agents/*.md        | ---> | artifacts (sdd/mem) |
| "o que executar"   |      | "como executar"    |      | "o que foi gravado" |
+--------------------+      +--------------------+      +---------------------+
           ^                           |                           |
           |                           v                           v
           |                 +--------------------+      +---------------------+
           +-----------------| PROJECT_RULES.md   |<-----| WORKFLOW_CONTRACTS  |
                             | regras normativas  |      | contrato de fluxo   |
                             +--------------------+      +---------------------+
```

## 3) Ordem mental para leitura de um leigo

```text
1) README.md
2) PROJECT_RULES.md
3) .claude/project-memory/current-state.md
4) .claude/project-memory/roadmap.json
5) docs/getting-started/README.md
6) docs/reference/README.md
```

## 4) Mapa estrutural resumido

```text
agentspec/
{tree}
```

## 5) Inventario completo de arquivos funcionais

| Arquivo | Para que serve |
|---|---|
{rows}

## 6) Como usar skills (instalada vs nao instalada)

```text
CASO A - Skill instalada:
- aparece na lista de skills da sessao
- possui SKILL.md acessivel
- pode ser invocada no fluxo da tarefa

CASO B - Skill nao instalada:
- nao aparece na lista de skills da sessao
- ou SKILL.md nao pode ser lido
- deve seguir fallback: comandos/agentes locais + docs do projeto
```

Em termos praticos, a base ja funciona sem skill extra, porque os comportamentos principais estao em:
- `.claude/commands/`
- `.claude/agents/`
- `.claude/sdd/`
- `.claude/project-memory/`

## 7) O que pode ser eliminado no seu cotidiano

### Manter (nucleo)
- `PROJECT_RULES.md`
- `.claude/sdd/`
- `.claude/project-memory/`
- `.claude/commands/workflow/`
- `.claude/commands/project-memory/`

### Adaptar (depende do time)
- `.claude/agents/communication/`
- `.claude/commands/core/`
- `docs/tutorials/`

### Eliminar com baixo risco (se nao usar)
- dominios KB nao utilizados em `.claude/kb/`
- agentes nunca acionados no seu fluxo real
- conteudo duplicado de documentacao

## 8) Checklist final de entendimento

```text
[ ] Entendo o fluxo Q ponta a ponta
[ ] Sei onde fica o estado atual (current-state.md)
[ ] Sei onde ficam tarefas e status (roadmap.json)
[ ] Sei como registrar sessao (checkpoint)
[ ] Sei como validar conformidade (Compliance PASS/FAIL)
[ ] Sei o que manter/adaptar/eliminar
```
"""


def main() -> None:
    files = list_files()
    md = build_md(files)
    OUT.write_text(md, encoding="utf-8")
    print(f"Generated: {OUT}")


if __name__ == "__main__":
    main()


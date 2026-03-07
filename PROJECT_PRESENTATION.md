# PROJECT PRESENTATION

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
|-- .claude
    |-- agents
    |-- commands
    |-- kb
    |-- project-memory
    `-- sdd
|-- .gitignore
|-- CHANGELOG.md
|-- CLAUDE.md
|-- CONTRIBUTING.md
|-- docs
    |-- concepts
    |-- getting-started
    |-- README.md
    |-- reference
    `-- tutorials
|-- LICENSE
|-- PROJECT_PRESENTATION.md
|-- PROJECT_RULES.md
|-- Q_VISUAL_GUIDE.md
|-- README.md
|-- scripts
    `-- generate_project_presentation.py
`-- SECURITY.md
```

## 5) Inventario completo de arquivos funcionais

| Arquivo | Para que serve |
|---|---|
| `.claude/agents/README.md` | Catalogo dos agentes disponiveis. |
| `.claude/agents/_template.md` | Template para criar novo agente. |
| `.claude/agents/code-quality/code-cleaner.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/code-quality/code-documenter.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/code-quality/code-reviewer.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/code-quality/test-generator.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/communication/adaptive-explainer.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/communication/linear-project-manager.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/communication/meeting-analyst.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/communication/the-planner.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/exploration/codebase-explorer.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/exploration/kb-architect.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/operations/executive-status-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/operations/project-tracker-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/operations/roadmap-guardian-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/operations/session-analyst-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/operations/weekly-forecaster-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/workflow/brainstorm-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/workflow/build-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/workflow/define-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/workflow/design-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/workflow/iterate-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/agents/workflow/ship-agent.md` | Definicao de agente especializado (papel, gatilhos, processo, quality gate). |
| `.claude/commands/README.md` | Catalogo dos comandos slash. |
| `.claude/commands/core/memory.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/core/readme-maker.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/core/sync-context.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/knowledge/create-kb.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/project-memory/checkpoint.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/project-memory/forecast-week.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/project-memory/start-project.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/project-memory/status.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/review/review.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/brainstorm.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/build.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/create-pr.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/define.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/design.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/iterate.md` | Definicao de comando operacional em markdown. |
| `.claude/commands/workflow/ship.md` | Definicao de comando operacional em markdown. |
| `.claude/kb/README.md` | Como usar e manter a base de conhecimento. |
| `.claude/kb/_index.yaml` | Indice dos dominios KB. |
| `.claude/kb/_templates/concept.md.template` | Template de dominio da base de conhecimento. |
| `.claude/kb/_templates/domain-manifest.yaml.template` | Template de dominio da base de conhecimento. |
| `.claude/kb/_templates/index.md.template` | Template de dominio da base de conhecimento. |
| `.claude/kb/_templates/pattern.md.template` | Template de dominio da base de conhecimento. |
| `.claude/kb/_templates/quick-reference.md.template` | Template de dominio da base de conhecimento. |
| `.claude/kb/_templates/spec.yaml.template` | Template de dominio da base de conhecimento. |
| `.claude/kb/_templates/test-case.json.template` | Template de dominio da base de conhecimento. |
| `.claude/project-memory/README.md` | Guia da camada de memoria operacional. |
| `.claude/project-memory/checkpoints/.gitkeep` | Placeholder para manter pasta versionada. |
| `.claude/project-memory/current-state.md` | Foto atual para retomar trabalho rapido. |
| `.claude/project-memory/metrics/progress-snapshot.json` | Snapshot de progresso global e por area. |
| `.claude/project-memory/metrics/weekly-metrics.json` | Metricas e previsao semanal. |
| `.claude/project-memory/project-manifest.md` | Objetivo, guardrails e direcao do projeto. |
| `.claude/project-memory/reports/executive-status.md` | Resumo executivo para decisores. |
| `.claude/project-memory/roadmap.json` | Plano por areas com status e dependencias. |
| `.claude/project-memory/sessions/.gitkeep` | Placeholder para manter pasta versionada. |
| `.claude/project-memory/templates/checkpoint-template.md` | Template da camada de memoria operacional. |
| `.claude/project-memory/templates/forecast-template.md` | Template da camada de memoria operacional. |
| `.claude/project-memory/templates/manifest-template.md` | Template da camada de memoria operacional. |
| `.claude/project-memory/templates/session-template.md` | Template da camada de memoria operacional. |
| `.claude/project-memory/templates/status-template.md` | Template da camada de memoria operacional. |
| `.claude/sdd/README.md` | Guia da camada SDD. |
| `.claude/sdd/_index.md` | Mapa resumido da camada SDD. |
| `.claude/sdd/architecture/ARCHITECTURE.md` | Visao arquitetural do metodo. |
| `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml` | Contrato de fases, gates e padroes. |
| `.claude/sdd/archive/.gitkeep` | Placeholder para manter pasta versionada. |
| `.claude/sdd/features/.gitkeep` | Placeholder para manter pasta versionada. |
| `.claude/sdd/reports/.gitkeep` | Placeholder para manter pasta versionada. |
| `.claude/sdd/templates/BRAINSTORM_TEMPLATE.md` | Template de artefato da fase SDD. |
| `.claude/sdd/templates/BUILD_REPORT_TEMPLATE.md` | Template de artefato da fase SDD. |
| `.claude/sdd/templates/DEFINE_TEMPLATE.md` | Template de artefato da fase SDD. |
| `.claude/sdd/templates/DESIGN_TEMPLATE.md` | Template de artefato da fase SDD. |
| `.claude/sdd/templates/SHIPPED_TEMPLATE.md` | Template de artefato da fase SDD. |
| `.gitignore` | Ignora arquivos temporarios e de ambiente no Git. |
| `CHANGELOG.md` | Historico de versoes e mudancas. |
| `CLAUDE.md` | Bootstrap obrigatorio e regras para sessoes de IA. |
| `CONTRIBUTING.md` | Como contribuir sem quebrar os padroes da base. |
| `LICENSE` | Licenca legal de uso. |
| `PROJECT_PRESENTATION.md` | Guia visual e funcional para estudo da base. |
| `PROJECT_RULES.md` | Fonte normativa de governanca operacional (MUST/MUST NOT). |
| `Q_VISUAL_GUIDE.md` | Arquivo de suporte do framework. |
| `README.md` | Resumo executivo do projeto e fluxo principal. |
| `SECURITY.md` | Politica de seguranca e reporte de vulnerabilidades. |
| `docs/README.md` | Entrada da documentacao. |
| `docs/concepts/README.md` | Conceitos e modelo mental. |
| `docs/getting-started/README.md` | Passo a passo para comecar. |
| `docs/reference/README.md` | Referencia de comandos/agentes/templates. |
| `docs/tutorials/README.md` | Tutoriais de uso. |
| `scripts/generate_project_presentation.py` | Arquivo de suporte do framework. |

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

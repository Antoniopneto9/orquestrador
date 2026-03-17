---
name: feedback
description: Lê todos os feedbacks.txt pendentes das páginas do app Streamlit e implementa as correções
---

# Feedback Command

Processa todos os feedbacks pendentes das páginas do app e implementa as melhorias.

## Usage

```bash
/feedback          # Lê e implementa todos os feedbacks PENDENTES
```

---

## O que faz

1. **Varre** todos os `streamlit/pages/**/feedback.txt`
2. **Filtra** apenas linhas marcadas como `PENDENTE:`
3. **Implementa** cada correção nos arquivos corretos da página
4. **Marca** cada item como `RESOLVIDO [YYYY-MM-DD HH:MM]:` no feedback.txt
5. **Reporta** tabela final com o que foi feito

---

## Processo

```text
1. Glob: streamlit/pages/**/feedback.txt
2. Para cada arquivo:
   a. Ler conteúdo
   b. Filtrar linhas PENDENTE
3. Para cada feedback PENDENTE:
   a. Identificar página afetada
   b. Ler functions.py da página
   c. Implementar correção
   d. Substituir PENDENTE → RESOLVIDO no feedback.txt
4. Exibir relatório final
```

---

## Contexto do app

- Entry points: `streamlit/pages/N_nome/N_nome.py`
- Lógica: `streamlit/pages/N_nome/functions.py`
- Componentes compartilhados: `streamlit/utils/components.py`
- Dados: Excel via `streamlit/utils/xlsx_io.py`
- Feedbacks: `streamlit/pages/N_nome/feedback.txt`

Formato do feedback.txt:
```
[2026-03-17 14:32] PENDENTE: texto da melhoria
[2026-03-17 15:10] RESOLVIDO [2026-03-18 09:00]: texto da melhoria
```

---

## Agente responsável

Use o agente `feedback-implementer` localizado em:
`.claude/agents/operations/feedback-implementer.md`

Invocar com Task tool passando contexto completo de todos os feedbacks encontrados.

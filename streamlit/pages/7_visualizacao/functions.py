"""
functions.py — Business logic for the Visualizacao Diaria page.

Each function is one feature of the page. No global code — everything is inside functions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st


def renderizar_secao(title: str, content: str) -> None:
    """Feature: render one visualization section as a styled HTML card.

    Uses a dark card with an orange left border — designed for meditation reading.
    """
    st.markdown(
        f"""
        <div style="
            margin-bottom: 1.5rem;
            padding: 1.5rem 2rem;
            border-radius: 10px;
            background-color: #0e1117;
            border-left: 5px solid #e8735a;
            font-size: 1.15rem;
            line-height: 1.85;
            color: #f0f0f0;
        ">
            <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.8rem; color: #e8735a;">
                {title}
            </div>
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_todas_secoes() -> None:
    """Feature: render all 6 visualization sections in sequence.

    Each section corresponds to a pillar of the intentional season identity.
    """
    # Section 1 — Future morning
    renderizar_secao(
        "A manhã de março de 2027",
        "Você acorda sem odiar o dia. Sem o peso no peito da primeira hora. "
        "O alarme toca e você respira fundo — não por obrigação, mas porque o dia tem sentido. "
        "Você sabe quem é. Você sabe para onde vai. E isso muda tudo.",
    )

    # Section 2 — Identity and presence
    renderizar_secao(
        "Quem você é",
        "Você entra numa sala e as pessoas percebem. Não pela roupa, não pelo cargo — pela presença. "
        "Você olha nos olhos. As palavras saem certas. Você argumenta sem travar, discorda sem pedir desculpa, "
        "diz não sem precisar justificar. Você fala primeiro. Você é visto. Você é respeitado. "
        "Você é a referência que sempre soube que poderia ser.",
    )

    # Section 3 — Physical appearance and space
    renderizar_secao(
        "Como você está",
        "A roupa te representa. A pele cuidada, o cabelo no lugar, os dentes claros. "
        "Seu apartamento tem a sua cara — mobiliado do jeito que você escolheu, sem improviso. "
        "O seu corpo respeita você porque você o respeitou primeiro. "
        "Você olha no espelho e reconhece o homem que escolheu ser.",
    )

    # Section 4 — Career and financial life
    renderizar_secao(
        "Como você vive",
        "R$1.000.000 líquido na conta. Sem dívidas de consumo. "
        "Promovido. Reconhecido como referência em dados e IA no agronegócio. "
        "Pessoas pedem sua opinião. Você entrega valor antes mesmo de ser pedido. "
        "Você tem projetos próprios que geram renda. Você construiu isso com constância, não com sorte.",
    )

    # Section 5 — Emotional state
    renderizar_secao(
        "Como você se sente",
        "Leve. Com brilho nos olhos. Sem o peso que você carregou por anos. "
        "Sem a tristeza sem nome que aparecia à toa. "
        "Você sorri e é real. Você age e é intencional. "
        "Você dorme bem e acorda disposto. Você vive presente — sem fugir para telas, sem anestesiar.",
    )

    # Section 6 — Gratitude close
    renderizar_secao(
        "Gratidão",
        "Obrigado pela clareza. Obrigado pela força. "
        "Obrigado por este momento de silêncio onde tudo é possível. "
        "<br><br><strong style='font-size: 1.4rem;'>Já está feito.</strong>",
    )

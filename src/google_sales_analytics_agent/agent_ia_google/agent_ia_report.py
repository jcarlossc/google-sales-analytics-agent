from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import re

import pandas as pd
import matplotlib.pyplot as plt
import google.genai as genai

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

def get_agent_report(
    df: pd.DataFrame,
    metrics_df: pd.DataFrame,
    statistics_df: Dict[str, Any]
) -> None:
    


    # =====================================================
    # CONFIGURAÇÕES
    # =====================================================
    OUTPUT_DIR = Path("reports")

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    PDF_FILE = OUTPUT_DIR / "relatorio_financeiro.pdf"

    GRAPH_FILE_RECEITA_MENSAL = OUTPUT_DIR / "receita_mensal.png"

    API_KEY = "API_KEY"

    # =====================================================
    # CONFIGURAR GEMINI
    # =====================================================

    client = genai.Client(
        api_key = API_KEY
    )

    #response = client.models.generate_content(
    #    model="gemini-2.5-flash",
    #    contents=prompt
    #)

     # -----------------------------------
    # CONVERTE metrics_df PARA DICT
    # -----------------------------------

    metrics = dict(
        zip(
            metrics_df["metrica"],
            metrics_df["valor"]
        )
    )

    faturamento = metrics[
        "faturamento_total"
    ]

    lucro = metrics[
        "lucro_total"
    ]

    margem = metrics[
        "margem_percentual"
    ]

    # -----------------------------------
    # ESTATÍSTICAS
    # -----------------------------------

    total_registros = statistics_df[
        "total_registros"
    ]

    primeira_venda = statistics_df[
        "data_venda"
    ][
        "primeira_venda"
    ]

    ultima_venda = statistics_df[
        "data_venda"
    ][
        "ultima_venda"
    ]

    media_qtd = statistics_df[
        "quantidade_vendida"
    ][
        "media"
    ]

    top_produto = statistics_df[
        "produto"
    ][
        "produto_mais_vendido"
    ]

    # -----------------------------------
    # GRÁFICO
    # -----------------------------------

    base = df.copy()

    base["faturamento"] = (

        base["quantidade_vendida"]

        *

        base["valor_venda"]

    )

    receita_mes = (

        base.groupby(

            base["data_venda"].dt.month

        )["faturamento"]

        .sum()

    )

    plt.figure(
        figsize=(8,5)
    )

    plt.plot(
        receita_mes.index,
        receita_mes.values,
        marker="o"
    )

    plt.grid()

    plt.savefig(
        GRAPH_FILE_RECEITA_MENSAL
    )

    plt.close()

    # -----------------------------------
    # PROMPT
    # -----------------------------------

    prompt = f"""
    Você é analista estatístico e financeiro.

    MÉTRICAS:

    Faturamento total: {faturamento}

    Lucro total: {lucro}

    Margem percentual: {margem:.2f}%

    Total registros: {total_registros}

    Primeira venda: {primeira_venda}

    Última venda: {ultima_venda}

    Média quantidade vendida: {media_qtd}

    Produto mais vendido: {top_produto}

    Retorne exatamente neste formato:

    INTRODUCAO:
    texto

    INTERPRETACAO_ESTATISTICA:
    texto

    CONCLUSAO_ESTATISTICA:
    texto

    INTERPRETACAO_FINANCEIRA:
    texto

    CONCLUSAO_FINANCEIRA:
    texto

    INSIGHTS:
    texto

    CONCLUSAO_FINAL:
    texto

    Não invente números.
    Use linguagem executiva.

    Retorne apenas texto puro.

    NÃO use:

    # títulos
    **
    *
    -
    markdown
    listas markdown

    Use somente texto simples e dividir os parágrafor com quebra de linha.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    texto = response.text


    # =====================================================
    # EXTRATOR DE SEÇÕES
    # =====================================================

    def extrair_secao(
        texto: str,
        inicio: str,
        fim: str | None = None
    ):

        if fim:

            padrao = rf"{inicio}:(.*?){fim}:"

        else:

            padrao = rf"{inicio}:(.*)"

        resultado = re.search(
            padrao,
            texto,
            re.S
        )

        if resultado:

            return resultado.group(
                1
            ).strip()

        return "Não encontrado"


    introducao = extrair_secao(
        texto,
        "INTRODUCAO",
        "INTERPRETACAO_ESTATISTICA"
    )

    estatistica = extrair_secao(
        texto,
        "INTERPRETACAO_ESTATISTICA",
        "CONCLUSAO_ESTATISTICA"
    )

    conclusao_est = extrair_secao(
        texto,
        "CONCLUSAO_ESTATISTICA",
        "INTERPRETACAO_FINANCEIRA"
    )

    financeira = extrair_secao(
        texto,
        "INTERPRETACAO_FINANCEIRA",
        "CONCLUSAO_FINANCEIRA"
    )

    conclusao_fin = extrair_secao(
        texto,
        "CONCLUSAO_FINANCEIRA",
        "INSIGHTS"
    )

    insights = extrair_secao(
        texto,
        "INSIGHTS",
        "CONCLUSAO_FINAL"
    )

    conclusao_final = extrair_secao(
        texto,
        "CONCLUSAO_FINAL"
    )


    # =====================================================
    # PDF
    # =====================================================

    styles = getSampleStyleSheet()

    story = []


    # -----------------------------------------------------
    # PÁGINA 1 - CAPA
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "RELATÓRIO ESTATÍSTICO E FINANCEIRO",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1,80)
    )

    story.append(
        Paragraph(
            f"Gerado em {datetime.now():%d/%m/%Y}",
            styles["Heading2"]
        )
    )

    story.append(
        Spacer(1,50)
    )

    story.append(
        Paragraph(
            "Projeto de Análise Automatizada",
            styles["BodyText"]
        )
    )

    story.append(
        PageBreak()
    )


    # -----------------------------------------------------
    # PÁGINA 2 - SUMÁRIO
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "SUMÁRIO",
            styles["Heading1"]
        )
    )

    itens = [
        "1. Introdução",
        "2. Interpretação Estatística",
        "3. Interpretação Financeira",
        "4. Insights",
        "5. Conclusão"
    ]

    for item in itens:

        story.append(
            Paragraph(
                item,
                styles["BodyText"]
            )
        )

    story.append(
        PageBreak()
    )


    # -----------------------------------------------------
    # PÁGINA 3 - INTRODUÇÃO
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "INTRODUÇÃO",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            introducao.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    story.append(
        PageBreak()
    )


    # -----------------------------------------------------
    # PÁGINA 4 - ESTATÍSTICA
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "INTERPRETAÇÃO ESTATÍSTICA",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            estatistica,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "CONCLUSÃO ESTATÍSTICA",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            conclusao_est,
            styles["BodyText"]
        )
    )

    story.append(
        PageBreak()
    )


    # -----------------------------------------------------
    # PÁGINA 5 - FINANCEIRO
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "INTERPRETAÇÃO FINANCEIRA",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            financeira,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "CONCLUSÃO FINANCEIRA",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            conclusao_fin,
            styles["BodyText"]
        )
    )

    story.append(
        PageBreak()
    )


    # -----------------------------------------------------
    # PÁGINA 6 - INSIGHTS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "INSIGHTS",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            insights,
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Image(
            str(GRAPH_FILE_RECEITA_MENSAL),
            width=450,
            height=250
        )
    )

    story.append(
        PageBreak()
    )


    # -----------------------------------------------------
    # PÁGINA 7 - CONCLUSÃO
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "CONCLUSÃO",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            conclusao_final,
            styles["BodyText"]
        )
    )


    # =====================================================
    # GERAR PDF
    # =====================================================

    doc = SimpleDocTemplate(
        str(PDF_FILE)
    )

    doc.build(
        story
    )

    print(
        f"PDF criado: {PDF_FILE}"
    )


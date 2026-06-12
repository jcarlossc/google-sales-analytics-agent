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
from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs

def get_agent_report(
    metrics_df: pd.DataFrame,
    statistics_df: Dict[str, Any]
) -> None:

    metrics = dict(
    zip(
        metrics_df["metrica"],
        metrics_df["valor"]
        )
    )

    config_path = Path("config")

    configs = load_all_configs(config_path)

    # =====================================================
    # CONFIGURAÇÕES
    # =====================================================
    OUTPUT_DIR = Path("reports")

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    PDF_FILE = OUTPUT_DIR / "relatorio_financeiro.pdf"

    GRAPH_FILE_INDICADORES = OUTPUT_DIR / "indicadores.png"
    GRAPH_FILE_MARGEM = OUTPUT_DIR / "margem.png"
    GRAPH_FILE_DISTRIBUICAO = OUTPUT_DIR / "distribuicao.png"

    API_KEY = configs["api_google"]["api"]["api_google"]

    # =====================================================
    # CONFIGURAR GEMINI
    # =====================================================
    client = genai.Client(
        api_key = API_KEY
    )

    # =====================================================
    # MÉTRICAS
    # =====================================================
    faturamento = metrics["faturamento_total"]
    custo = metrics["custo_total"]
    lucro = metrics["lucro_total"]
    margem = metrics["margem_percentual"]

    # =====================================================
    # ESTATÍSTICAS
    # =====================================================
    total_registros = statistics_df["total_registros"]
    data_venda = statistics_df["data_venda"]
    primeira_venda = statistics_df["data_venda"]["primeira_venda"]
    ultima_venda = statistics_df["data_venda"]["ultima_venda"]
    dias_periodo = statistics_df["data_venda"]["dias_periodo"]
    mes_mais_vendas = statistics_df["data_venda"]["mes_mais_vendas"]
    quantidade_vendida_media = statistics_df["quantidade_vendida"]["media"]
    quantidade_vendida_mediana = statistics_df["quantidade_vendida"]["mediana"]
    quantidade_vendida_desvio = statistics_df["quantidade_vendida"]["desvio_padrao"]
    quantidade_vendida_minimo = statistics_df["quantidade_vendida"]["minimo"]
    quantidade_vendida_q1 = statistics_df["quantidade_vendida"]["q1"]
    quantidade_vendida_q3 = statistics_df["quantidade_vendida"]["q3"]
    quantidade_vendida_maximo = statistics_df["quantidade_vendida"]["maximo"]
    produtos_unicos = statistics_df["produto"]["produtos_unicos"]
    produto_mais_vendido = statistics_df["produto"]["produto_mais_vendido"]
    produto_top_5_produtos = statistics_df["produto"]["top_5_produtos"]
    valor_compra_media = statistics_df["valor_compra"]["media"]
    valor_compra_mediana = statistics_df["valor_compra"]["mediana"]
    valor_compra_desvio = statistics_df["valor_compra"]["desvio"]
    valor_compra_q1 = statistics_df["valor_compra"]["q1"]
    valor_compra_q3 = statistics_df["valor_compra"]["q3"]
    valor_venda_media = statistics_df["valor_venda"]["media"]
    valor_venda_mediana = statistics_df["valor_venda"]["mediana"]
    valor_venda_total_faturado = statistics_df["valor_venda"]["total_faturado"]
    total_faturado_maximo = statistics_df["valor_venda"]["maximo"]

    # -----------------------------------
    # GRÁFICOS
    # Faturamento, custo e lucro
    # -----------------------------------
    valores = [
        faturamento,
        custo,
        lucro
    ]
    labels = [
        "Faturamento",
        "Custo",
        "Lucro"
    ]    
    fig, ax = plt.subplots(
    figsize=(8, 5)
    )

    bars = ax.bar(
        labels,
        valores
    )

    ax.set_title(
        "Indicadores Financeiros"
    )

    ax.set_ylabel(
        "Valor (R$)"
    )

    for bar in bars:

        altura = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            altura,
            f"R$ {altura:,.0f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    plt.savefig(
        GRAPH_FILE_INDICADORES,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------------
    # Margem
    # -----------------------------------
    plt.figure(figsize=(6, 4))

    bars = plt.bar(
        ["Margem de Lucro"],
        [margem]
    )

    # Exibe o valor acima da barra
    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{margem:.2f}%",
            ha="center",
            va="bottom"
        )

    plt.title("Margem de Lucro (%)")
    plt.ylabel("Percentual (%)")
    plt.ylim(0, max(margem * 1.2, 10))
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(GRAPH_FILE_MARGEM, dpi=300, bbox_inches="tight")
    plt.close()

    # -----------------------------------
    # Distribuição da Quantidade Vendida
    # -----------------------------------
    valores = [
    statistics_df["quantidade_vendida"]["minimo"],
    statistics_df["quantidade_vendida"]["q1"],
    statistics_df["quantidade_vendida"]["mediana"],
    statistics_df["quantidade_vendida"]["q3"],
    statistics_df["quantidade_vendida"]["maximo"]
    ]

    labels = [
        "Mínimo",
        "Q1",
        "Mediana",
        "Q3",
        "Máximo"
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        labels,
        valores,
        marker="o",
        linewidth=2
    )

    # Exibe os valores em cada ponto
    for x, y in zip(labels, valores):
        plt.annotate(
            f"{y:.0f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center"
        )

    plt.title("Distribuição da Quantidade Vendida")
    plt.xlabel("Medidas Estatísticas")
    plt.ylabel("Quantidade")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(GRAPH_FILE_DISTRIBUICAO, dpi=300, bbox_inches="tight")
    plt.close()

     # -----------------------------------
    # PROMPT
    # -----------------------------------
    prompt = f"""
    Você é analista estatístico e financeiro.

    MÉTRICAS:

    Faturamento total: {faturamento}

    Custo: {custo}

    Lucro total: {lucro}

    Margem percentual: {margem:.2f}%

    Total registros: {total_registros}

    Primeira venda: {primeira_venda}

    Última venda: {ultima_venda}

    Períodos em dias: {dias_periodo}

    Mês com mais vendas: {mes_mais_vendas}

    Média quantidade vendida: {quantidade_vendida_media}

    Mediana quantidade vendida: {quantidade_vendida_mediana}

    Desvio padrão quantidade vendida: {quantidade_vendida_desvio}

    Quantidade mínima vendida: {quantidade_vendida_minimo}

    Quantidade máxima vendida: {quantidade_vendida_maximo}

    Primeiro quartil quantidade vendida: {quantidade_vendida_q1}

    Terceiro quartil quantidade vendida: {quantidade_vendida_q3}

    Produtos únicos: {produtos_unicos}

    Produtos mais vendido: {produto_mais_vendido}

    Produto mais vendido: {produto_top_5_produtos}

    Média do valor das compras: {valor_compra_media}

    Mediana do valor das compras: {valor_compra_mediana}

    Desvio padrão do valor das compras: {valor_compra_desvio}

    Primeiro quartil do valor das compras: {valor_compra_q1}

    Terceiro quartil do valor das compras: {valor_compra_q3}

    Média do valor das vendas: {valor_venda_media}

    Mediana do valor das vendas: {valor_venda_mediana}

    Valor total faturado: {valor_venda_total_faturado}

    Total máximo faturado: {total_faturado_maximo}

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
            str(GRAPH_FILE_INDICADORES),
            width=450,
            height=250
        )
    )

    story.append(
        Image(
            str(GRAPH_FILE_MARGEM),
            width=450,
            height=250
        )
    )

    story.append(
        Image(
            str(GRAPH_FILE_DISTRIBUICAO),
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
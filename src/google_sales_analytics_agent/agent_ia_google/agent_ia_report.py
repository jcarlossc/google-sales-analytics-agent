from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import re

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import google.genai as genai
import logging

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
    metrics_df: Dict[str, Any],
    statistics_df: Dict[str, Any]
) -> None:
    
    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info("Início da geração do relatório.")    

    # Carregamento de arquivos de configuração
    config_path = Path("config")

    configs = load_all_configs(config_path)

    # -----------------------------------
    # CONFIGURAÇÕES
    # -----------------------------------
    # Diretório do relatório
    OUTPUT_DIR = Path("reports")

    # Cria diretório caso não exista
    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    # Arquivo PDF
    PDF_FILE = OUTPUT_DIR / "relatorio_financeiro.pdf"

    # Arquivos de imagens
    GRAPH_FILE_INDICADORES = OUTPUT_DIR / "indicadores.png"
    GRAPH_FILE_TOP_SELLER = OUTPUT_DIR / "top_seller.png"
    GRAPH_FILE_TOP_PRODUCTS = OUTPUT_DIR / "top_products.png"

    # Chave de agente IA Google
    API_KEY = configs["api_google"]["api"]["api_google"]

    # -----------------------------------
    # CONFIGURAR GEMINI
    # -----------------------------------
    client = genai.Client(
        api_key = API_KEY
    )

    # -----------------------------------
    # MÉTRICAS
    # -----------------------------------
    total_vendas = metrics_df["kpis"]["total_vendas"]
    total_itens_vendidos = metrics_df["kpis"]["total_itens_vendidos"]
    faturamento_total = metrics_df["kpis"]["faturamento_total"]
    custo_total = metrics_df["kpis"]["custo_total"]
    lucro_total = metrics_df["kpis"]["lucro_total"]
    margem = metrics_df["kpis"]["margem"]
    ticket_medio = metrics_df["kpis"]["ticket_medio"]
    qtd_produtos = metrics_df["kpis"]["qtd_produtos"]
    qtd_vendedores = metrics_df["kpis"]["qtd_vendedores"]
    by_seller = metrics_df["by_seller"]
    by_product = metrics_df["by_product"]

    # -----------------------------------
    # ESTATÍSTICAS
    # -----------------------------------
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
    # Faturamento, custo, lucro e ticket
    # -----------------------------------
    valores = [
        faturamento_total,
        custo_total,
        lucro_total,
        ticket_medio
    ]
    labels = [
        "Faturamento",
        "Custo",
        "Lucro",
        "Ticket Médio"
    ]    
    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(labels,valores)

    # Título
    ax.set_title(
        "Indicadores Financeiros",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.set_ylabel("Valor (R$)")

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
    # Top 10 vendedores
    # -----------------------------------
    top_sellers = (
        by_seller
        .head(10)
        .sort_values("faturamento")
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    norm = mcolors.Normalize(
        vmin=top_sellers["faturamento"].min(),
        vmax=top_sellers["faturamento"].max()
    )

    colors = cm.Blues(
        norm(top_sellers["faturamento"])
    )

    bars = ax.barh(
        top_sellers["vendedor"],
        top_sellers["faturamento"],
        color=colors,
        edgecolor="black"
    )

    max_value = top_sellers["faturamento"].max()

    for bar in bars:
        value = bar.get_width()
        ax.text(
            value * 1.01,
            bar.get_y() + bar.get_height()/2,
            f"R$ {value:,.2f}".replace(",", "X")
                                  .replace(".", ",")
                                  .replace("X", "."),
            va="center",
            fontsize=9,
            fontweight="bold"
        )

    ax.set_title(
        "Top 10 Vendedores",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Faturamento")

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    plt.savefig(
        GRAPH_FILE_TOP_SELLER,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------------
    # Top 10 produtos
    # -----------------------------------
    top_products = (
        by_product
        .head(10)
        .sort_values(
            "faturamento"
        )
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    # Gradiente de cores
    norm = mcolors.Normalize(
        vmin=top_products["faturamento"].min(),
        vmax=top_products["faturamento"].max()
    )

    colors = cm.Blues(
        norm(
            top_products["faturamento"]
        )
    )

    # Barras horizontais
    bars = ax.barh(
        top_products["produto"],
        top_products["faturamento"],
        color=colors,
        edgecolor="black",
        linewidth=0.8
    )

    # Valores nas barras
    for bar in bars:
        valor = bar.get_width()
        ax.text(
            valor * 1.01,
            bar.get_y() + bar.get_height()/2,
            (
                f"R$ {valor:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            ),
            va="center",
            fontsize=9,
            fontweight="bold"
        )

    # Título
    ax.set_title(
        "Top 10 Produtos",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.text(
        0.5,
        1.02,
        "Ranking dos produtos com maior faturamento",
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        color="gray"
    )

    ax.set_xlabel(
        "Faturamento (R$)",
        fontsize=11,
        fontweight="bold"
    )

    ax.set_ylabel(
        "Produto",
        fontsize=11,
        fontweight="bold"
    )

    # Grid
    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    # Limpeza visual
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    plt.savefig(
        GRAPH_FILE_TOP_PRODUCTS,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------------
    # PROMPT
    # -----------------------------------
    prompt = f"""
    Você é analista estatístico e financeiro.

    MÉTRICAS:

    Total de vendas: {total_vendas}

    Total de itens vendidos: {total_itens_vendidos}

    Faturamento total: {faturamento_total}

    Custo: {custo_total}

    Lucro total: {lucro_total}

    Ticket médio: {ticket_medio}

    Quantidade de produtos: {qtd_produtos}

    Quantidade de vendedores: {qtd_vendedores}

    Faturamento por produto : {by_product}

    Faturamento por vendedor : {by_seller}

    Margem percentual: {margem}

    Total registros: {total_registros}

    Datas vendas: {data_venda}

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

    # -----------------------------------
    # EXTRATOR DE SEÇÕES
    # -----------------------------------
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

    # -----------------------------------
    # PDF
    # -----------------------------------
    styles = getSampleStyleSheet()

    story = []

    # -----------------------------------
    # PÁGINA 1 - CAPA
    # -----------------------------------
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
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(0,50)
    )

    story.append(
        Paragraph(
            "Projeto de Análise Automatizada",
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(0,50)
    )

    story.append(
        Paragraph(
            "Relatório gerado do Projeto Google Sales Analytics Agent",
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(0,50)
    )

    story.append(
        Paragraph(
            "Autor: Carlos da Costa",
            styles["BodyText"]
        )
    )

    story.append(
        PageBreak()
    )

    # -----------------------------------
    # PÁGINA 2 - SUMÁRIO
    # -----------------------------------
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
        "6. Conclusão"
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

    # -----------------------------------
    # PÁGINA 3 - INTRODUÇÃO
    # -----------------------------------
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


    # -----------------------------------
    # PÁGINA 4 - ESTATÍSTICA
    # -----------------------------------
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


    # -----------------------------------
    # PÁGINA 5 - FINANCEIRO
    # -----------------------------------
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


    # -----------------------------------
    # PÁGINA 6 - INSIGHTS
    # -----------------------------------
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
            str(GRAPH_FILE_TOP_SELLER),
            width=450,
            height=250
        )
    )

    story.append(
        Spacer(1,50)
    )

    story.append(
        Image(
            str(GRAPH_FILE_TOP_PRODUCTS),
            width=450,
            height=250
        )
    )

    story.append(
        PageBreak()
    )

    # -----------------------------------
    # PÁGINA 7 - CONCLUSÃO
    # -----------------------------------
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

    # -----------------------------------
    # GERAR PDF
    # -----------------------------------
    doc = SimpleDocTemplate(str(PDF_FILE))

    doc.build(story)

    print(f"PDF criado: {PDF_FILE}")

    logger.info("Término da geração do relatório.")  
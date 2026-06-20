import logging
import pandas as pd
from typing import Dict, Any

def calculate_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula métricas gerais de vendas
    e retorna resultados em DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Base padronizada de vendas.

    Returns
    -------
    Dict
        Dicionário contendo métricas
        consolidadas.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    try:
        logger.info("Calculando métricas.")

        # ------------------------------------------------------
        # Métricas derivadas
        # ------------------------------------------------------
        df_metrics = df.copy()

        df_metrics["faturamento"] = (
            df_metrics["quantidade_vendida"]
            * df_metrics["valor_venda"]
        )

        df_metrics["custo_total"] = (
            df_metrics["quantidade_vendida"]
            * df_metrics["valor_compra"]
        )

        df_metrics["lucro"] = (
            df_metrics["faturamento"]
            - df_metrics["custo_total"]
        )

        # ------------------------------------------------------
        # KPIs gerais
        # ------------------------------------------------------
        kpis = {
            "total_vendas": len(df_metrics),

            "total_itens_vendidos":
                df_metrics["quantidade_vendida"].sum(),

            "faturamento_total":
                df_metrics["faturamento"].sum(),

            "custo_total":
                df_metrics["custo_total"].sum(),

            "lucro_total":
                df_metrics["lucro"].sum(),

            "margem":
                (df_metrics["lucro"] / df_metrics["faturamento"]) * 100,

            "ticket_medio":
                df_metrics["faturamento"].mean(),

            "qtd_produtos":
                df_metrics["produto_id"].nunique(),

            "qtd_vendedores":
                df_metrics["vendedor_id"].nunique()
        }

        # ------------------------------------------------------
        # Métricas por vendedor
        # ------------------------------------------------------
        by_seller = (
            df_metrics
            .groupby(
                ["vendedor_id", "vendedor"],
                as_index=False
            )
            .agg(
                vendas=("vendedor_id", "count"),
                itens_vendidos=("quantidade_vendida", "sum"),
                faturamento=("faturamento", "sum"),
                lucro=("lucro", "sum")
            )
            .sort_values(
                by="faturamento",
                ascending=False
            )
        )

        # ------------------------------------------------------
        # Métricas por produto
        # ------------------------------------------------------

        by_product = (
            df_metrics
            .groupby(
                ["produto_id", "produto"],
                as_index=False
            )
            .agg(
                vendas=("produto_id", "count"),
                itens_vendidos=("quantidade_vendida", "sum"),
                faturamento=("faturamento", "sum"),
                lucro=("lucro", "sum")
            )
            .sort_values(
                by="faturamento",
                ascending=False
            )
        )

        logger.info("Métricas calculadas.")

        # ------------------------------------------------------
        # Retorno
        # ------------------------------------------------------
        return {
            "status": "sucesso",
            "mensagem": "Métricas calculadas com sucesso.",
            "kpis": kpis,
            "by_seller": by_seller,
            "by_product": by_product
        }

    except Exception:
        logger.exception(
            "Erro ao calcular métricas."
        )
        raise
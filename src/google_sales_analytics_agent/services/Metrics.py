import logging
import pandas as pd


def calculate_metrics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula métricas gerais de vendas
    e retorna resultados em DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Base padronizada de vendas.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo métricas
        consolidadas.
    """

    logger = logging.getLogger(__name__)

    try:

        logger.info(
            "Calculando métricas."
        )

        base = df.copy()

        faturamento = float(
            (
                base["quantidade_vendida"]
                *
                base["valor_venda"]
            ).sum()
        )

        custo = float(
            (
                base["quantidade_vendida"]
                *
                base["valor_compra"]
            ).sum()
        )

        lucro = faturamento - custo

        margem_pct = (
            (lucro / faturamento) * 100
            if faturamento != 0
            else 0
        )

        metrics_df = pd.DataFrame({

            "metrica": [

                "faturamento_total",
                "custo_total",
                "lucro_total",
                "margem_percentual"

            ],

            "valor": [

                faturamento,
                custo,
                lucro,
                margem_pct

            ]

        })

        logger.info(
            "Métricas calculadas."
        )

        return metrics_df

    except Exception:

        logger.exception(
            "Erro ao calcular métricas."
        )

        raise
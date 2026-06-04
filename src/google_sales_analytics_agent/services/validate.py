import logging
from typing import Dict, Any
import pandas as pd

def validate_sales_data(
    df: pd.DataFrame
) -> Dict[str, Any]:
   

    logger = logging.getLogger(__name__)

    logger.info(
        "Iniciando validação de qualidade."
    )

    try:

        if df.empty:

            raise ValueError(
                "Dataset vazio."
            )

        quality_report = {}

        # Mede quantidade de valores ausentes.
        quality_report["missing_values"] = (
            df.isna()
            .sum()
            .to_dict()
        )

        logger.info(
            f"Valores ausentes: "
            f"{quality_report['missing_values']}"
        )

        # Mede duplicidade completa.
        quality_report["duplicates"] = int(
            df.duplicated().sum()
        )

        logger.info(
            f"Valores duplicados: "
            f"{quality_report['duplicates']}"
        )

        # Quantidade vendida deve ser positiva.
        quality_report[
            "invalid_quantity"
        ] = int(
            (df["quantidade_vendida"] <= 0)
            .sum()
        )

        logger.info(
            f"Valores negativos: "
            f"{quality_report['invalid_quantity']}"
        )

        # Valores monetários não devem ser negativos.
        quality_report[
            "negative_purchase_price"
        ] = int(
            (df["valor_compra"] < 0)
            .sum()
        )

        logger.info(
            f"Valor de compra negativo: "
            f"{quality_report['negative_purchase_price']}"
        )

        quality_report[
            "negative_sale_price"
        ] = int(
            (df["valor_venda"] < 0)
            .sum()
        )

        logger.info(
            f"Valor de venda negativo: "
            f"{quality_report['negative_sale_price']}"
        )

        # Data inválida após conversão.
        quality_report[
            "invalid_dates"
        ] = int(
            df["data_venda"]
            .isna()
            .sum()
        )

        logger.info(
            f"Datas inválidas: "
            f"{quality_report['invalid_dates']}"
        )

        # Detecta prejuízo por item.
        quality_report[
            "negative_margin"
        ] = int(
            (
                df["valor_venda"]
                <
                df["valor_compra"]
            ).sum()
        )

        logger.info(
            f"Margem negativa: "
            f"{quality_report['negative_margin']}"
        )

        logger.info(
            "Validação concluída."
        )

        return quality_report

    except ValueError as error:

        logger.warning(
            str(error)
        )

        raise

    except Exception:

        logger.exception(
            "Erro durante validação."
        )

        raise
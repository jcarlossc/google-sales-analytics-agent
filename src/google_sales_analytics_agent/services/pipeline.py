from pathlib import Path
import pandas as pd
from typing import Dict, Any, Tuple
import logging

from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs
from google_sales_analytics_agent.utils.loggers.logger import setup_logger
from google_sales_analytics_agent.database.connection import get_engine
from google_sales_analytics_agent.database.load_sales import get_load_sales
from google_sales_analytics_agent.services.standardization import standardize_sales_data
from google_sales_analytics_agent.services.validate import validate_sales_data
from google_sales_analytics_agent.services.metrics import calculate_metrics
from google_sales_analytics_agent.services.statistic import descriptive_statistics
from google_sales_analytics_agent.agent_ia_google.agent_ia_report import get_agent_report

def run_pipeline() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Executa pipeline completo de análise de vendas.

    Fluxo:
    1. Carrega configurações
    2. Configura logging
    3. Cria conexão banco
    4. Extrai dados
    5. Padroniza dados
    6. Valida dataset
    7. Calcula métricas
    8. Calcula estatísticas
    9. Finaliza recursos

    Returns
    -------
    Tuple[Dict[str, Any], Dict[str, Any]]
        sales_metrics:
            Métricas financeiras e comerciais.

        statistics:
            Estatísticas descritivas.

    Raises
    ------
    RuntimeError
        Caso alguma etapa do pipeline falhe.
    """

    logger = logging.getLogger(__name__)

    conn = None

    pd.set_option(
        "display.float_format",
        "{:,.2f}".format
    )

    try:
        # -------------------------
        # Logger
        # -------------------------
        logger.info(
            "Carregando arquivos de configutação."
        )

        config_path = Path("config")

        configs = load_all_configs(config_path)

        # -------------------------
        # Logger
        # -------------------------
        logger.info("Criando logger.")

        setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

        logger.info("### Iniciando pipeline de vendas. ###")
        
        # -------------------------
        # Conexão banco
        # -------------------------
        logger.info("Criando conexão com banco.")

        conn = get_engine(configs["db"]["database"])

        # -------------------------
        # Extração
        # -------------------------
        logger.info("Carregando dados.")

        queries = get_load_sales(conn)

        # -------------------------
        # Transformação
        # -------------------------
        logger.info("Padronizando dados.")

        standardization = standardize_sales_data(queries)

        # -------------------------
        # Validação
        # -------------------------

        logger.info("Validando dados.")

        df = validate_sales_data(standardization)

        # -------------------------
        # Métricas
        # -------------------------
        logger.info("Processando métricas.")

        metrics_df = calculate_metrics(df)

        print(metrics_df)

        # -------------------------
        # Estatística
        # -------------------------
        logger.info("Processando estatísticas.")

        statistics_df = descriptive_statistics(df)

        print(statistics_df)

        # -------------------------
        # Agente IA Google
        # -------------------------
        get_agent_report(
            df,
            metrics_df,
            statistics_df
        )

        logger.info("### Término do pipeline de vendas. ###")

        #return (metrics, statistics)

    except Exception as erro:

        logger.exception(
            "Falha durante execução do pipeline."
        )

        raise RuntimeError(
            f"Erro no pipeline: {erro}"
        ) from erro

    finally:

        if conn is not None:

            logger.info(
                "Fechando conexão."
            )

            conn.dispose()

        logger.info(
            "### Pipeline finalizado ###"
        )


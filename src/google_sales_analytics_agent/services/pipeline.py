from pathlib import Path
import logging
from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs
from google_sales_analytics_agent.utils.loggers.logger import setup_logger
from google_sales_analytics_agent.database.connection import get_engine
from google_sales_analytics_agent.database.load_sales import get_load_sales
from google_sales_analytics_agent.services.standardization import standardize_sales_data
from google_sales_analytics_agent.services.validate import validate_sales_data
from google_sales_analytics_agent.services.Metrics import Metrics
from google_sales_analytics_agent.services.statistic import descriptive_statistics

def run_pipeline() ->None:

    config_path = Path("config")

    configs = load_all_configs(config_path)


    setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

    logger = logging.getLogger(__name__)

    logger.info("### Iniciando pipeline de vendas. ###")
    
    conn = get_engine(configs["db"]["database"])

    queries = get_load_sales(conn)

    standardization = standardize_sales_data(queries)

    df = validate_sales_data(standardization)

    metrics = Metrics(df)

    sales_metrics = {
        "faturamento": metrics.total_invoicing(),
        "custo": metrics.total_cost(),
        "lucro": metrics.total_profit(),
        "porcentagem_margem": metrics.percentage_margin(),
        "vendas_mes": metrics.sales_month(),
        "top_vendedore": metrics.top_sellers(),
        "top_produtos": metrics.top_products()
    }

    statistics = descriptive_statistics(df)

    conn.dispose()

    logger.info("### Término do pipeline de vendas. ###")

    return sales_metrics, statistics




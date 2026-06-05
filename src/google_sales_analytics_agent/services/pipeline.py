from pathlib import Path
import logging
from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs
from google_sales_analytics_agent.utils.loggers.logger import setup_logger
from google_sales_analytics_agent.database.connection import get_engine
from google_sales_analytics_agent.database.load_sales import get_load_sales
from google_sales_analytics_agent.services.standardization import standardize_sales_data
from google_sales_analytics_agent.services.validate import validate_sales_data
from google_sales_analytics_agent.services.Metrics import Metrics

def run_pipeline() ->None:

    config_path = Path("config")

    configs = load_all_configs(config_path)


    setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

    logger = logging.getLogger(__name__)

    logger.info("### Iniciando pipeline de vendas. ###")
    

    conn = get_engine(configs["db"]["database"])

    print(conn)

    queries = get_load_sales(conn)

    standardization = standardize_sales_data(queries)

    df = validate_sales_data(standardization)

    metrics = Metrics(df)
    print(metrics.total_invoicing())
    print(metrics.total_cost())
    print(metrics.total_profit())
    print(metrics.percentage_margin())
    print(metrics.sales_month())
    print(metrics.top_sellers())
    print(metrics.top_products())

    conn.dispose()

    logger.info("### Término do pipeline de vendas. ###")


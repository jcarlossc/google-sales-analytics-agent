from pathlib import Path
import logging
from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs
from google_sales_analytics_agent.utils.loggers.logger import setup_logger
from google_sales_analytics_agent.database.connection import get_engine

def run_pipeline() ->None:

    config_path = Path("config")

    configs = load_all_configs(config_path)


    setup_logger(configs["logging"], configs["paths"]["logs"]["file"])

    logger = logging.getLogger(__name__)

    logger.info("### Iniciando pipeline de vendas. ###")
    

    conn = get_engine(configs["db"]["database"])

    print(conn)

    conn.dispose()

    logger.info("### Término do pipeline de vendas. ###")


"""
Ponto de entrada principal da aplicação.

Este módulo é responsável por iniciar o pipeline principal
de análise de vendas. A execução é iniciada chamando a função
`main()`, que delega o processamento para o pipeline central.

Uso
---
    poetry run vendas
"""

from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs
from google_sales_analytics_agent.utils.loggers.logger import setup_logger
from google_sales_analytics_agent.services.pipeline import run_pipeline

def main() -> None:
    """
    Executa o pipeline principal da aplicação.

    Esta função atua como ponto central de inicialização,
    delegando a execução ao pipeline responsável pelas
    etapas de processamento, análise e geração de resultados.

    Retorno
    -------
    None
        A função apenas executa o fluxo principal da aplicação.
    """

    run_pipeline()

if __name__ == "__main__":
    main()
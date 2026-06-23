from unittest.mock import patch, MagicMock
from google_sales_analytics_agent.services.pipeline import run_pipeline

def test_run_pipeline_execucao_com_sucesso():
    """
    Verifica se o pipeline executa todas
    as etapas corretamente.
    """

    # -----------------------------
    # Arrange
    # Preparação dos dados simulados
    # -----------------------------

    configs_mock = {

        "logging": {
            "level": "INFO",
            "format": "%(message)s"
        },

        "paths": {
            "logs": {
                "file": "logs/app.log"
            }
        },

        "db": {
            "database": {
                "user": "root",
                "password": "123",
                "host": "localhost",
                "db": "sales"
            }
        }
    }

    # Simula conexão com banco
    engine_mock = MagicMock()

    # Simula DataFrame carregado
    df_mock = MagicMock()

    # -----------------------------
    # Act
    # Execução do pipeline
    # -----------------------------

    with patch(
        "google_sales_analytics_agent.services.pipeline.load_all_configs",
        return_value=configs_mock
    ), patch(
        "google_sales_analytics_agent.services.pipeline.setup_logger"
    ), patch(
        "google_sales_analytics_agent.services.pipeline.get_engine",
        return_value=engine_mock
    ), patch(
        "google_sales_analytics_agent.services.pipeline.get_load_sales",
        return_value=df_mock
    ), patch(
        "google_sales_analytics_agent.services.pipeline.standardize_sales_data",
        return_value=df_mock
    ), patch(
        "google_sales_analytics_agent.services.pipeline.validate_sales_data",
        return_value=(df_mock, {})
    ), patch(
        "google_sales_analytics_agent.services.pipeline.calculate_metrics",
        return_value={}
    ), patch(
        "google_sales_analytics_agent.services.pipeline.descriptive_statistics",
        return_value={}
    ), patch(
        "google_sales_analytics_agent.services.pipeline.get_agent_report"
    ):

        resultado = run_pipeline()

    # -----------------------------
    # Assert
    # Verificação
    # -----------------------------

    # run_pipeline não possui retorno
    assert resultado is None

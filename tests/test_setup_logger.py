from google_sales_analytics_agent.utils.loggers.logger import setup_logger

def test_setup_logger_cria_arquivo_log(tmp_path):
    """
    Verifica se o logger é configurado e
    se o arquivo de log é criado.
    """

    # Arrange (Preparação)

    # Configuração mínima necessária para o logger
    logging_config = {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        }
    }

    # Arquivo de log temporário criado pelo pytest
    log_file = tmp_path / "logs" / "app.log"

    # Act (Execução)

    setup_logger(
        logging_config=logging_config,
        log_file=str(log_file)
    )

    # Assert (Verificação)

    # Verifica se a pasta foi criada
    assert log_file.parent.exists()

    # Verifica se o arquivo de log foi criado
    assert log_file.exists()
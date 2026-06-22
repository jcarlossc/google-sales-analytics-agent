from pathlib import Path

from google_sales_analytics_agent.utils.load_config.loader_config import load_all_configs

def test_load_all_configs_retorna_dicionario():
    """
    Verifica se a função retorna um dicionário
    ao carregar um arquivo YAML válido.
    """

    # Diretório de teste contendo arquivos YAML
    config_path = Path("config")

    # Executa a função que será testada
    resultado = load_all_configs(config_path)

    # Verifica se o retorno é um dicionário
    assert isinstance(resultado, dict)

    # Verifica se a configuração "api_google"
    # foi carregada para o dicionário
    assert "api_google" in resultado

    # Verifica se a configuração "db"
    # foi carregada para o dicionário
    assert "db" in resultado

    # Verifica se a configuração "paths"
    # foi carregada para o dicionário
    assert "paths" in resultado

    # Verifica se a configuração "logging"
    # foi carregada para o dicionário
    assert "logging" in resultado
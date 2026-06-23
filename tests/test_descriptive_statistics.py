import pandas as pd
from google_sales_analytics_agent.services.statistic import descriptive_statistics

def test_descriptive_statistics_retorna_estatisticas():
    """
    Verifica se a função calcula corretamente
    algumas estatísticas descritivas.
    """

    # Arrange (Preparação)
    # Cria um DataFrame pequeno para teste.
    df = pd.DataFrame(
        {
            "vendas_id": [1, 2, 3],
            "data_venda": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03"
                ]
            ),
            "produto": [
                "Notebook",
                "Mouse",
                "Notebook"
            ],
            "quantidade_vendida": [2, 4, 6],
            "valor_compra": [1000, 20, 1000],
            "valor_venda": [1500, 50, 1500]
        }
    )

    # Act (Execução)
    resultado = descriptive_statistics(df)

    # Assert (Verificação)

    # Verifica se retornou um dicionário
    assert isinstance(resultado, dict)

    # Verifica total de registros
    assert resultado["total_registros"] == 3

    # Verifica média da quantidade vendida
    assert (
        resultado["quantidade_vendida"]["media"]
        == 4.0
    )

    # Verifica produto mais vendido
    assert (
        resultado["produto"]["produto_mais_vendido"]
        == "Notebook"
    )

    # Verifica quantidade de produtos únicos
    assert (
        resultado["produto"]["produtos_unicos"]
        == 2
    )
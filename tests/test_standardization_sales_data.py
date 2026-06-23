import pandas as pd

from google_sales_analytics_agent.services.standardization import standardize_sales_data


def test_standardize_sales_data():
    """
    Verifica se os dados são padronizados
    corretamente.
    """

    # Arrange (Preparação)

    # Cria DataFrame com dados "sujos"
    df = pd.DataFrame(
        {
            "vendas_id": ["1", "1"],
            "data_venda": ["2024-01-01", "2024-01-01"],
            "quantidade_vendida": ["10", "10"],
            "produto": [" Notebook ", " Notebook "],
            "valor_compra": ["1000", "1000"],
            "valor_venda": ["1500", "1500"],
            "vendedor": [" Carlos ", " Carlos "]
        }
    )

    # Act (Execução)

    resultado = standardize_sales_data(df)

    # Assert (Verificação)

    # Deve remover registro duplicado
    assert len(resultado) == 1

    # Deve remover espaços e converter para minúsculo
    assert resultado["produto"].iloc[0] == "notebook"

    # Deve remover espaços e converter para minúsculo
    assert resultado["vendedor"].iloc[0] == "carlos"

    # Deve converter para datetime
    assert pd.api.types.is_datetime64_any_dtype(
        resultado["data_venda"]
    )
import pandas as pd
from google_sales_analytics_agent.services.validate import validate_sales_data

def test_validate_sales_data_retorna_relatorio_qualidade():
    """
    Verifica se a função identifica problemas
    de qualidade dos dados corretamente.
    """

    # Arrange (Preparação)

    # Cria DataFrame com alguns problemas:
    #
    # - quantidade negativa
    # - valor de venda negativo
    # - valor ausente
    # - margem negativa
    # - data inválida
    #
    df = pd.DataFrame(
        {
            "vendas_id": [1, 2, 3],

            "data_venda": pd.to_datetime(
                [
                    "2024-01-01",
                    None,
                    "2024-01-03"
                ]
            ),

            "quantidade_vendida": [
                10,
                -5,
                3
            ],

            "valor_compra": [
                100,
                200,
                300
            ],

            "valor_venda": [
                150,
                -50,
                200
            ]
        }
    )

    # Act (Execução)

    resultado_df, quality_report = (
        validate_sales_data(df)
    )

    # Assert (Verificação)

    # Verifica se o primeiro retorno
    # continua sendo um DataFrame
    assert isinstance(
        resultado_df,
        pd.DataFrame
    )

    # Verifica se o segundo retorno
    # é um dicionário
    assert isinstance(
        quality_report,
        dict
    )

    # Verifica quantidade de valores ausentes
    assert (
        quality_report["missing_values"]["data_venda"]
        == 1
    )

    # Verifica quantidade vendida inválida
    # (-5 é menor que zero)
    assert (
        quality_report["invalid_quantity"]
        == 1
    )

    # Verifica venda com valor negativo
    assert (
        quality_report["negative_sale_price"]
        == 1
    )

    # Verifica margem negativa
    # venda menor que custo
    assert (
        quality_report["negative_margin"]
        == 2
    )
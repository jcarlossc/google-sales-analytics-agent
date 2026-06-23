import pandas as pd
from google_sales_analytics_agent.services.metrics import calculate_metrics

def test_calculate_metrics_retorna_metricas():
    """
    Verifica se a função calcula as métricas
    corretamente a partir de um DataFrame válido.
    """

    # Arrange (Preparação)
    # Cria um DataFrame simples para o teste.
    df = pd.DataFrame(
        {
            "produto_id": [1, 2],
            "produto": ["Notebook", "Mouse"],
            "vendedor_id": [10, 20],
            "vendedor": ["Carlos", "Ana"],
            "quantidade_vendida": [2, 5],
            "valor_compra": [1000, 20],
            "valor_venda": [1500, 50]
        }
    )

    # Act (Execução)
    resultado = calculate_metrics(df)

    # Assert (Verificação)

    # Verifica se retornou um dicionário
    assert isinstance(resultado, dict)

    # Verifica o status da operação
    assert resultado["status"] == "sucesso"

    # Recupera os KPIs calculados
    kpis = resultado["kpis"]

    # Verifica quantidade de vendas
    assert kpis["total_vendas"] == 2

    # Verifica total de itens vendidos
    assert kpis["total_itens_vendidos"] == 7

    # Verifica quantidade de produtos distintos
    assert kpis["qtd_produtos"] == 2

    # Verifica quantidade de vendedores distintos
    assert kpis["qtd_vendedores"] == 2
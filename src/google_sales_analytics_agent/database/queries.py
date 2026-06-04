import pandas as pd

def load_sales(engine):
    
    query = """
    SELECT

    v.vendas_id,
    v.data_venda,
    v.quantidade_vendida,

    p.produto,
    p.valor_compra,
    p.valor_venda,

    vd.vendedor

    FROM vendas v

    JOIN produto p
    ON v.produto_id = p.produto_id

    JOIN vendedor vd
    ON v.vendedor_id = vd.vendedor_id
    """

    return pd.read_sql(
        query,
        engine
    )
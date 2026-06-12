import logging
from typing import Dict #, Any, List
import pandas as pd

def descriptive_statistics(df: pd.DataFrame) -> Dict:
    """
    Gera estatísticas descritivas para dataset de vendas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo vendas.

    Returns
    -------
    Dict[str, Any]
    """

    logger = logging.getLogger(__name__)

    logger.info("Calculando Estatística Descritiva.")

    try:

        if df.empty:
            raise ValueError(
                "DataFrame vazio."
            )

        statistics_df = {

            "total_registros": df["vendas_id"].count(),

            "data_venda": {

                "primeira_venda":
                    str(df["data_venda"].min()),

                "ultima_venda":
                    str(df["data_venda"].max()),

                "dias_periodo":
                    (
                        df["data_venda"].max()
                        -
                        df["data_venda"].min()
                    ).days,

                "mes_mais_vendas":
                    df["data_venda"]
                    .dt.month
                    .mode()[0]
            },

            "quantidade_vendida": {

                "media":
                    round(
                        df["quantidade_vendida"].mean(),
                        2
                    ),

                "mediana":
                    df["quantidade_vendida"].median(),

                "desvio_padrao":
                    round(
                        df["quantidade_vendida"].std(),
                        2
                    ),

                "minimo": df["quantidade_vendida"].min(),  

                "q1": df["quantidade_vendida"].quantile( 0.25 ), 
                
                "q3": df["quantidade_vendida"].quantile( 0.75 ), 
                
                "maximo": df["quantidade_vendida"].max()  
            },

            "produto": {
                "produtos_unicos":
                    df["produto"].nunique(),

                "produto_mais_vendido":
                    df["produto"]
                    .mode()[0],
                    
                "top_5_produtos": 
                    df["produto"] .value_counts() .head(5)    
            },

            "valor_compra": {
                "media": round( df["valor_compra"].mean(), 2 ), 
                
                "mediana": df["valor_compra"].median(), 
                
                "desvio": round( df["valor_compra"].std(), 2 ), 
                
                "q1": df["valor_compra"].quantile( 0.25 ), 
                
                "q3": df["valor_compra"].quantile( 0.75 ),  
            },

            "valor_venda" : {
                "media": round( df["valor_venda"].mean(), 2 ), 
                
                "mediana": df["valor_venda"].median(), 
                
                "total_faturado": round( ( df["valor_venda"] * df["quantidade_vendida"] ).sum(), 2 ), 
                
                "maximo": df["valor_venda"].max() 
            }

        }

        logger.info("Término do cálculo de Estatística Descritiva.")

        return statistics_df

    except Exception as erro:

        raise RuntimeError(
            f"Erro estatístico: {erro}"
        ) from erro
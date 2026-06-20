import logging
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

def get_load_sales(engine: Engine) -> pd.DataFrame:
    """
    Carrega dados consolidados de vendas
    a partir do banco de dados.

    A consulta realiza junção entre tabelas
    de vendas, produtos e vendedores para
    construção da base analítica.

    Parameters
    ----------
    engine : Engine
        Instância SQLAlchemy Engine utilizada
        para comunicação com banco.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo dados de vendas.

    Raises
    ------
    SQLAlchemyError
        Quando ocorre falha na consulta SQL.

    ValueError
        Quando o resultado retornado está vazio.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info(
        "Iniciando carregamento dos dados de vendas."
    )

    # Consulta utilizada para consolidar
    # informações de vendas, produtos e vendedores.
    query = """
    SELECT

    v.vendas_id,
    v.data_venda,

    v.produto_id,
    v.vendedor_id,

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

    try:
        # Executa consulta SQL e converte
        # resultado para DataFrame Pandas.
        df = pd.read_sql(
            query,
            engine
        )

        # Evita continuar pipeline
        # com base vazia.
        if df.empty:
            logger.warning(
                "Consulta retornou dataset vazio."
            )

            raise ValueError(
                "Nenhum registro encontrado."
            )

        logger.info(f"{len(df)} registros carregados.")

        return df

    except SQLAlchemyError as error:
        logger.error(
            f"Erro ao executar consulta SQL: {error}"
        )
        raise

    except Exception as error:
        logger.exception(
            "Erro inesperado ao carregar vendas."
        )
        raise
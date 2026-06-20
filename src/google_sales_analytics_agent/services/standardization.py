import logging
import pandas as pd

def standardize_sales_data(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Realiza padronização dos dados de vendas.

    Etapas executadas:
    - valida colunas obrigatórias
    - converte tipos de dados
    - remove espaços extras
    - padroniza texto
    - trata valores ausentes

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto de vendas.

    Returns
    -------
    pd.DataFrame
        DataFrame padronizado.

    Raises
    ------
    KeyError
        Quando colunas obrigatórias estão ausentes.

    ValueError
        Quando transformação falha.

    Exception
        Para erros inesperados.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info(
        "Iniciando padronização dos dados."
    )

    # Colunas a serem padronizadas
    required_columns = [
        "vendas_id",
        "data_venda",
        "quantidade_vendida",
        "produto",
        "valor_compra",
        "valor_venda",
        "vendedor"
    ]

    try:
        # Verifica se todas as colunas
        # necessárias existem.
        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:
            logger.warning(
                f"Colunas ausentes: {missing}"
            )

            raise KeyError(
                f"Colunas obrigatórias ausentes: {missing}"
            )

        # Cria cópia para evitar alterar
        # objeto original.
        df = df.copy()

        # Converte identificador para inteiro.
        df["vendas_id"] = (
            pd.to_numeric(
                df["vendas_id"],
                errors="coerce"
            )
            .astype("Int64")
        )

        # Converte datas.
        df["data_venda"] = pd.to_datetime(
            df["data_venda"],
            errors="coerce"
        )

        # Converte variáveis numéricas.
        numeric_cols = [
            "quantidade_vendida",
            "valor_compra",
            "valor_venda"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        # Remove espaços extras
        # e padroniza textos.
        text_cols = [
            "produto",
            "vendedor"
        ]

        for col in text_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # Remove duplicidades.
        before = len(df)

        df = df.drop_duplicates()

        removed = before - len(df)

        logger.info(
            f"{removed} duplicatas removidas."
        )

        logger.info(
            "Padronização concluída."
        )

        return df

    except KeyError as error:
        logger.warning(
            f"Erro de estrutura: {error}"
        )
        raise

    except ValueError as error:
        logger.error(
            f"Erro de transformação: {error}"
        )
        raise

    except Exception as error:
        logger.exception(
            "Erro inesperado durante padronização."
        )
        raise
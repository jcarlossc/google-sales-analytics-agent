from typing import Dict, Any
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

def get_engine(config: Dict[str, Any]) -> Engine:
    """
    Cria e retorna uma instância SQLAlchemy Engine
    utilizando configurações de conexão.

    Parameters
    ----------
    config : Dict[str, Any]
        Dicionário contendo:
        - user
        - password
        - host
        - db

    Returns
    -------
    Engine
        Engine SQLAlchemy configurada.

    DatabaseError
        Para erros inesperados.
    """

    # Recupera logger do módulo atual para
    # rastreamento do fluxo de execução.
    logger = logging.getLogger(__name__)

    logger.info("Iniciando criação da engine.")

    try:
        
        # Monta string de conexão utilizada
        # pelo SQLAlchemy para acessar MySQL.
        conn=(
          f"mysql+pymysql://"
          f"{config['user']}:"
          f"{config['password']}@"
          f"{config['host']}:3306/"
          f"{config['db']}"
        )

        # Cria instância Engine responsável
        engine = create_engine(conn)

        logger.info("Engine criada com sucesso.")

        return engine
    
    except KeyError as error:
        logger.warning(f"Parâmetro obrigatório ausente: {error}")

        raise KeyError(
            f"Parâmetro obrigatório ausente: {error}"
        ) from error

    except SQLAlchemyError as error:
        logger.error(f"Erro ao criar engine: {error}")

        raise
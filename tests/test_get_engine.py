from sqlalchemy.engine import Engine
from google_sales_analytics_agent.database.connection import get_engine

def test_get_engine_cria_engine():
    """
    Verifica se a função cria corretamente
    um objeto SQLAlchemy Engine.
    """

    # Arrange (Preparação)
    # Configuração fictícia de conexão.
    # Não precisa existir um banco real.
    config = {
        "user": "root",
        "password": "123456",
        "host": "localhost",
        "db": "sales"
    }

    # Act (Execução)
    engine = get_engine(config)

    # Assert (Verificação)

    # Verifica se o retorno é uma Engine SQLAlchemy
    assert isinstance(engine, Engine)

    # Verifica se a URL de conexão foi montada corretamente
    assert engine.url.drivername == "mysql+pymysql"

    assert engine.url.username == "root"
    assert engine.url.host == "localhost"
    assert engine.url.database == "sales"
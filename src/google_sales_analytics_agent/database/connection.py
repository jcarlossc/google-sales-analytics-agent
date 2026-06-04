from sqlalchemy import create_engine

def get_engine(config):

    try:
        conn=(
          f"mysql+pymysql://"
          f"{config['user']}:"
          f"{config['password']}@"
          f"{config['host']}:3306/"
          f"{config['db']}"
        )

        return create_engine(conn)
    
    except KeyError as error:

        raise KeyError(
            f"Parâmetro obrigatório ausente: {error}"
        ) from error
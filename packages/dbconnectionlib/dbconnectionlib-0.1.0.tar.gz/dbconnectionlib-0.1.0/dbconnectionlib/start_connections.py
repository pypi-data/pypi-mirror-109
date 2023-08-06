import sqlalchemy
from sqlalchemy import create_engine


def init_connection_engine(db_user, db_pass, db_name, db_socket_dir, cloud_sql_connection_name):
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    }

    return init_unix_connection_engine(db_config, db_user, db_pass, db_name, db_socket_dir, cloud_sql_connection_name)


def init_unix_connection_engine(db_config,db_user, db_pass, db_name, db_socket_dir, cloud_sql_connection_name):
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgres+pg8000",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,
                    cloud_sql_connection_name)
            }
        ),
        **db_config
    )

    return pool


def init_tcp_connection(db_user, db_pass, db_name, cloud_sql_connection_name):
    """
    Create connection to the db using CP protocols
    Returns: db connection
    """
    engine_string = "postgresql+psycopg2://%s:%s@%s:%d/%s" \
                    % (db_user, db_pass,
                       cloud_sql_connection_name, 5432,
                       db_name)

    return create_engine(engine_string)

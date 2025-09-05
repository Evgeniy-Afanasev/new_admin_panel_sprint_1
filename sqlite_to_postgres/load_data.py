import os
import sqlite3
import psycopg
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row
from dotenv import load_dotenv
from contextlib import closing
import logging
from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader

load_dotenv()

logging.basicConfig(filename="logger.log", level=logging.INFO)
log = logging.getLogger()


def load_from_sqlite(sq3_conn: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(sq3_conn)

    data = sqlite_loader.load_data()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER', default='app'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST', default='127.0.0.1'),
        'port': os.environ.get('POSTGRES_PORT', default=5432),
        'options': '-c search_path=public,content',
    }

    try:
        with closing(sqlite3.connect('db.sqlite')) as sqlite_conn, closing(psycopg.connect( **dsl, row_factory=dict_row, cursor_factory=ClientCursor)) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except sqlite3.Error as e:
        log.exception(f'SQLite Error\n{e}\n')
    except psycopg.DatabaseError as e:
        log.exception(f'PostgreSQL\n{e}\n')
    except Exception as e:
        log.exception(e)
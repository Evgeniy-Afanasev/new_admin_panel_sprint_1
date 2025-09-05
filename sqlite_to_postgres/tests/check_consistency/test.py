import os
from dotenv import load_dotenv
import sqlite3
import psycopg
from psycopg.rows import dict_row
from datetime import datetime
from uuid import UUID


load_dotenv()


SQLITE_PATH = '../../db.sqlite'
POSTGRES_DSL = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER', default='app'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST', default='127.0.0.1'),
    'port': os.environ.get('POSTGRES_PORT', default=5432),
    'options': '-c search_path=public,content',
}


TABLES = [
    'genre',
    'film_work',
    'person',
    'genre_film_work',
    'person_film_work',
]


def fetch_all_rows_sqlite(cursor, table):
    cursor.execute(f'SELECT * FROM {table}')
    return cursor.fetchall()


def fetch_all_rows_postgres(cursor, table):
    cursor.execute(f'SELECT * FROM content.{table}')
    return cursor.fetchall()

def normalize_row(row: dict) -> dict:
    result = {}
    for k, v in row.items():
        if isinstance(v, datetime):
            result[k] = v.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(v, UUID):
            result[k] = str(v)
        elif isinstance(v, str) and k.endswith('_at'):
            result[k] = v[:19]
        else:
            if v is not None:
                result[k] = str(v)
            else:
                result[k] = None
    return result

def test_tables_match():
    with sqlite3.connect(SQLITE_PATH) as sqlite_conn, psycopg.connect(**POSTGRES_DSL, row_factory=dict_row) as postgres_conn:
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cur = sqlite_conn.cursor()
        postgres_cur = postgres_conn.cursor()

        for table in TABLES:
            sqlite_rows = fetch_all_rows_sqlite(sqlite_cur, table)
            postgres_rows = fetch_all_rows_postgres(postgres_cur, table)

            assert len(sqlite_rows) == len(postgres_rows), f"Расхождение количества строк в таблице '{table}'"

            sqlite_dicts = sorted([normalize_row(dict(row)) for row in sqlite_rows], key=lambda r: r['id'])
            postgres_dicts = sorted([normalize_row(row) for row in postgres_rows], key=lambda r: r['id'])

            for row_sqlite, row_postgres in zip(sqlite_dicts, postgres_dicts):
                assert row_sqlite == row_postgres, f"Расхождение данных в таблице '{table}' - ID {row_sqlite['id']}"


if __name__ == '__main__':
    test_tables_match()
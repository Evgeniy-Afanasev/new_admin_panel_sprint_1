from sqlite3 import Connection
from table_classes import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork


class SQLiteLoader:
    def __init__(self, conn: Connection):
        self.conn = conn

    def load_data(self) -> dict:
        return {
            'film_work': self._load_table('film_work', FilmWork),
            'genre': self._load_table('genre', Genre),
            'person': self._load_table('person', Person),
            'genre_film_work': self._load_table('genre_film_work', GenreFilmWork),
            'person_film_work': self._load_table('person_film_work', PersonFilmWork),
        }

    def _load_table(self, table_name, model_cls, block_size=100):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [column[0] for column in cursor.description]

        while True:
            rows = cursor.fetchmany(block_size)
            if not rows:
                break
            yield [model_cls(**dict(zip(columns, row))) for row in rows]

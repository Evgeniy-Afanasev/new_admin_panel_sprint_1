from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    creation_date: date
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Person:
    id: str
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created_at: datetime


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime
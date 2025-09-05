CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    modified timestamp with time zone DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    genre_id uuid NOT NULL REFERENCES content.genre ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work ON DELETE CASCADE,
    created timestamp with time zone DEFAULT NOW(),
    UNIQUE (genre_id, film_work_id)
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id uuid NOT NULL REFERENCES content.person ON DELETE CASCADE,
    film_work_id uuid NOT NULL REFERENCES content.film_work ON DELETE CASCADE,
    role TEXT NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    UNIQUE (person_id, film_work_id, role)
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_rating_idx ON content.film_work (creation_date, rating);
CREATE INDEX IF NOT EXISTS film_work_creation_date_type_idx ON content.film_work (creation_date, type);

CREATE UNIQUE INDEX IF NOT EXISTS genre_name_idx ON content.genre (name);
CREATE UNIQUE INDEX IF NOT EXISTS person_full_name_idx ON content.person (full_name);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);
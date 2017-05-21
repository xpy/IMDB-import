-- Table: movie

DROP TABLE IF EXISTS movie CASCADE;

-- Sequence: movie_id_seq

DROP SEQUENCE IF EXISTS movie_id_seq;

CREATE SEQUENCE movie_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1424628
  CACHE 1;
ALTER TABLE movie_id_seq
  OWNER TO postgres;

CREATE TABLE movie
(
  id integer NOT NULL DEFAULT nextval('movie_id_seq'::regclass),
  name text,
  year integer,
  year_id smallint,
  rating double precision,
  votes integer,
  CONSTRAINT movie_id PRIMARY KEY (id),
  CONSTRAINT "UC_movie__name__year__year_id" UNIQUE (name, year, year_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE movie
  OWNER TO postgres;

-- Index: "IX_movie__id"

DROP INDEX IF EXISTS "IX_movie__id";

CREATE UNIQUE INDEX "IX_movie__id"
  ON movie
  USING btree
  (id);
ALTER TABLE movie CLUSTER ON "IX_movie__id";

-- Index: "IX_movie__name__year__year_id"

DROP INDEX IF EXISTS "IX_movie__name__year__year_id";

CREATE UNIQUE INDEX "IX_movie__name__year__year_id"
  ON movie
  USING btree
  (name COLLATE pg_catalog."default", year, year_id);


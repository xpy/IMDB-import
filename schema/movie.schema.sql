-- Table: public.movie

DROP TABLE IF EXISTS public.movie CASCADE;

-- Sequence: public.movie_id_seq

DROP SEQUENCE IF EXISTS public.movie_id_seq;

CREATE SEQUENCE public.movie_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1424628
  CACHE 1;
ALTER TABLE public.movie_id_seq
  OWNER TO postgres;

CREATE TABLE public.movie
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
ALTER TABLE public.movie
  OWNER TO postgres;

-- Index: public."IX_movie__id"

DROP INDEX IF EXISTS public."IX_movie__id";

CREATE UNIQUE INDEX "IX_movie__id"
  ON public.movie
  USING btree
  (id);
ALTER TABLE public.movie CLUSTER ON "IX_movie__id";

-- Index: public."IX_movie__name__year__year_id"

DROP INDEX IF EXISTS public."IX_movie__name__year__year_id";

CREATE UNIQUE INDEX "IX_movie__name__year__year_id"
  ON public.movie
  USING btree
  (name COLLATE pg_catalog."default", year, year_id);


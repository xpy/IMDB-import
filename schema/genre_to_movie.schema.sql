-- Table: public.genre_to_movie

DROP TABLE IF EXISTS public.genre_to_movie CASCADE;

-- Sequence: public.genre_to_movie_id_seq

DROP SEQUENCE IF EXISTS public.genre_to_movie_id_seq;

CREATE SEQUENCE public.genre_to_movie_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 2336696
  CACHE 1;
ALTER TABLE public.genre_to_movie_id_seq
  OWNER TO postgres;


CREATE TABLE public.genre_to_movie
(
  id integer NOT NULL DEFAULT nextval('genre_to_movie_id_seq'::regclass),
  genre_id integer,
  movie_id integer,
  CONSTRAINT "PK_genre_to_movie__id" PRIMARY KEY (id),
  CONSTRAINT "FK_genre_to_movie__genre" FOREIGN KEY (genre_id)
      REFERENCES public.genre (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT "FK_genre_to_movie__movie_id" FOREIGN KEY (movie_id)
      REFERENCES public.movie (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.genre_to_movie
  OWNER TO postgres;

-- Index: public."IX_genre_to_movie__genre_id__movie_id"

DROP INDEX IF EXISTS public."IX_genre_to_movie__genre_id__movie_id";

CREATE UNIQUE INDEX "IX_genre_to_movie__genre_id__movie_id"
  ON public.genre_to_movie
  USING btree
  (genre_id, movie_id);
ALTER TABLE public.genre_to_movie CLUSTER ON "IX_genre_to_movie__genre_id__movie_id";

-- Index: public."IX_genre_to_movie__id"

DROP INDEX IF EXISTS public."IX_genre_to_movie__id";

CREATE UNIQUE INDEX "IX_genre_to_movie__id"
  ON public.genre_to_movie
  USING btree
  (id);


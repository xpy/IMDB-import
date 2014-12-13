-- Table: genre_to_movie

-- DROP TABLE genre_to_movie;

CREATE TABLE genre_to_movie
(
  id serial NOT NULL,
  genre_id integer,
  movie_id integer,
  CONSTRAINT "PK_genre_to_movie__id" PRIMARY KEY (id),
  CONSTRAINT "FK_genre_to_movie__genre" FOREIGN KEY (genre_id)
      REFERENCES genre (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT "FK_genre_to_movie__movie_id" FOREIGN KEY (movie_id)
      REFERENCES movie (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE genre_to_movie
  OWNER TO postgres;

-- Index: "IX_genre_to_movie__genre_id__movie_id"

-- DROP INDEX "IX_genre_to_movie__genre_id__movie_id";

CREATE UNIQUE INDEX "IX_genre_to_movie__genre_id__movie_id"
  ON genre_to_movie
  USING btree
  (genre_id, movie_id);
ALTER TABLE genre_to_movie CLUSTER ON "IX_genre_to_movie__genre_id__movie_id";

-- Index: "IX_genre_to_movie__id"

-- DROP INDEX "IX_genre_to_movie__id";

CREATE UNIQUE INDEX "IX_genre_to_movie__id"
  ON genre_to_movie
  USING btree
  (id);


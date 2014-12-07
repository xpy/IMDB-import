-- Table: actor_to_movie

-- DROP TABLE actor_to_movie;

CREATE TABLE actor_to_movie
(
  id serial NOT NULL,
  actor_id integer,
  movie_id integer,
  CONSTRAINT "PK_actor_to_movie__id" PRIMARY KEY (id),
  CONSTRAINT "FK_actor_to_movie__actor_id" FOREIGN KEY (actor_id)
      REFERENCES actor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT "FK_actor_to_movie__movie_id" FOREIGN KEY (movie_id)
      REFERENCES movie (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT "UC_actor_to_movie__actor_id__movie_id" UNIQUE (actor_id, movie_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE actor_to_movie
  OWNER TO postgres;

-- Index: "IX_actor_to_movie__actor_id__movie_id"

-- DROP INDEX "IX_actor_to_movie__actor_id__movie_id";

CREATE UNIQUE INDEX "IX_actor_to_movie__actor_id__movie_id"
  ON actor_to_movie
  USING btree
  (actor_id, movie_id);
ALTER TABLE actor_to_movie CLUSTER ON "IX_actor_to_movie__actor_id__movie_id";


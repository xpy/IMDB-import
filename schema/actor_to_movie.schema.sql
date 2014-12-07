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
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE actor_to_movie
  OWNER TO postgres;

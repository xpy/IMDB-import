-- Table: actor_to_movie

DROP TABLE IF EXISTS actor_to_movie CASCADE;

-- Sequence: actor_to_movie_id_seq

DROP SEQUENCE IF EXISTS actor_to_movie_id_seq;

CREATE SEQUENCE actor_to_movie_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 169848
  CACHE 1;
ALTER TABLE actor_to_movie_id_seq
  OWNER TO postgres;

CREATE TABLE actor_to_movie
(
  id integer NOT NULL DEFAULT nextval('actor_to_movie_id_seq'::regclass),
  actor_id integer,
  movie_id integer,
  billing_position integer,
  roles text,
  role_id integer,
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

DROP INDEX IF EXISTS "IX_actor_to_movie__actor_id__movie_id";

CREATE UNIQUE INDEX "IX_actor_to_movie__actor_id__movie_id"
  ON actor_to_movie
  USING btree
  (actor_id, movie_id);
ALTER TABLE actor_to_movie CLUSTER ON "IX_actor_to_movie__actor_id__movie_id";


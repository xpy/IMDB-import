-- Table: movie

-- DROP TABLE movie;

CREATE TABLE movie
(
  id serial NOT NULL,
  name text,
  year integer,
  year_id text,
  rating double precision,
  votes integer,
  CONSTRAINT movie_id PRIMARY KEY (id),
  CONSTRAINT "UC_movie__name__year_id" UNIQUE (name, year_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE movie
  OWNER TO postgres;

-- Index: "IX_movie__id"

-- DROP INDEX "IX_movie__id";

CREATE UNIQUE INDEX "IX_movie__id"
  ON movie
  USING btree
  (id);
ALTER TABLE movie CLUSTER ON "IX_movie__id";

-- Index: "IX_movie__name__year_id"

-- DROP INDEX "IX_movie__name__year_id";

CREATE UNIQUE INDEX "IX_movie__name__year_id"
  ON movie
  USING btree
  (name COLLATE pg_catalog."default", year_id COLLATE pg_catalog."default");


-- Rule: "RL_movie__insert_duplicate" ON movie

-- DROP RULE "RL_movie__insert_duplicate" ON movie;

CREATE OR REPLACE RULE "RL_movie__insert_duplicate" AS
    ON INSERT TO movie
   WHERE (EXISTS ( SELECT 1
           FROM movie
          WHERE movie.name = new.name AND movie.year_id = new.year_id)) DO INSTEAD NOTHING;
ALTER TABLE movie DISABLE RULE "RL_movie__insert_duplicate";


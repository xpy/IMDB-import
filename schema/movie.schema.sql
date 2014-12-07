-- Table: movie

-- DROP TABLE movie;

CREATE TABLE movie
(
  id serial NOT NULL,
  name text,
  year integer,
  CONSTRAINT movie_id PRIMARY KEY (id),
  CONSTRAINT movie_name UNIQUE (name)
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

-- Index: "IX_movie__name"

-- DROP INDEX "IX_movie__name";

CREATE UNIQUE INDEX "IX_movie__name"
  ON movie
  USING btree
  (name COLLATE pg_catalog."default");


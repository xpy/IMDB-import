-- Table: actor

-- DROP TABLE actor;

CREATE TABLE actor
(
  id integer NOT NULL DEFAULT nextval('actors_id_seq'::regclass),
  name text,
  CONSTRAINT actor_id PRIMARY KEY (id),
  CONSTRAINT actor_name UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE actor
  OWNER TO postgres;

-- Index: "IX_actor__id"

-- DROP INDEX "IX_actor__id";

CREATE UNIQUE INDEX "IX_actor__id"
  ON actor
  USING btree
  (id);
ALTER TABLE actor CLUSTER ON "IX_actor__id";

-- Index: "IX_actor__name"

-- DROP INDEX "IX_actor__name";

CREATE UNIQUE INDEX "IX_actor__name"
  ON actor
  USING btree
  (name COLLATE pg_catalog."default");


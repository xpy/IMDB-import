-- Table: actor

-- DROP TABLE actor;

CREATE TABLE actor
(
  id integer NOT NULL DEFAULT nextval('actor_id_seq'::regclass),
  fname_id text,
  gender "char",
  CONSTRAINT actor_id PRIMARY KEY (id),
  CONSTRAINT "UC_actor__name__gender" UNIQUE (name, gender)
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

-- Index: "IX_actor__name__gender"

-- DROP INDEX "IX_actor__name__gender";

CREATE UNIQUE INDEX "IX_actor__name__gender"
  ON actor
  USING btree
  (name COLLATE pg_catalog."default", gender);


-- Table: actor

DROP TABLE IF EXISTS actor CASCADE;

-- Sequence: actor_id_seq

DROP SEQUENCE IF EXISTS actor_id_seq;

CREATE SEQUENCE actor_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 993
  CACHE 1;
ALTER TABLE actor_id_seq
  OWNER TO postgres;


CREATE TABLE actor
(
  id integer NOT NULL DEFAULT nextval('actor_id_seq'::regclass),
  name text,
  gender "char",
  fname_id integer,
  lname_id integer,
  name_index smallint,
  CONSTRAINT actor_id PRIMARY KEY (id),
  CONSTRAINT "FK_actor__fname_id" FOREIGN KEY (fname_id)
      REFERENCES actor_name (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_actor__lname_id" FOREIGN KEY (lname_id)
      REFERENCES actor_name (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "UC_actor__name__gender" UNIQUE (name, gender)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE actor
  OWNER TO postgres;

-- Index: "FKI_actor__fname_id"

DROP INDEX IF EXISTS "FKI_actor__fname_id";

CREATE INDEX "FKI_actor__fname_id"
  ON actor
  USING btree
  (fname_id);

-- Index: "FKI_actor__lname_id"

DROP INDEX IF EXISTS "FKI_actor__lname_id";

CREATE INDEX "FKI_actor__lname_id"
  ON actor
  USING btree
  (lname_id);

-- Index: "IX_actor__id"

DROP INDEX IF EXISTS "IX_actor__id";

CREATE UNIQUE INDEX "IX_actor__id"
  ON actor
  USING btree
  (id);
ALTER TABLE actor CLUSTER ON "IX_actor__id";

-- Index: "IX_actor__name__gender"

DROP INDEX IF EXISTS "IX_actor__name__gender";

CREATE UNIQUE INDEX "IX_actor__name__gender"
  ON actor
  USING btree
  (name COLLATE pg_catalog."default", gender);


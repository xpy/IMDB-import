-- Table: genre

-- DROP TABLE genre;

CREATE TABLE genre
(
  id smallint NOT NULL DEFAULT nextval('gender_id_seq'::regclass),
  name text,
  CONSTRAINT "PK_genre__id" PRIMARY KEY (id),
  CONSTRAINT "UC_genre__name" UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE genre
  OWNER TO postgres;

-- Index: "IX_genre__id"

-- DROP INDEX "IX_genre__id";

CREATE UNIQUE INDEX "IX_genre__id"
  ON genre
  USING btree
  (id);

-- Index: "IX_genre__name"

-- DROP INDEX "IX_genre__name";

CREATE UNIQUE INDEX "IX_genre__name"
  ON genre
  USING btree
  (name COLLATE pg_catalog."default");
ALTER TABLE genre CLUSTER ON "IX_genre__name";


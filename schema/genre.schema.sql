-- Table: genre

DROP TABLE IF EXISTS genre CASCADE;

-- Sequence: genre_id_seq

DROP SEQUENCE IF EXISTS genre_id_seq;

CREATE SEQUENCE genre_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 34
  CACHE 1;
ALTER TABLE genre_id_seq
  OWNER TO postgres;

CREATE TABLE genre
(
  id smallint NOT NULL DEFAULT nextval('genre_id_seq'::regclass),
  name text,
  is_movie_genre boolean,
  CONSTRAINT "PK_genre__id" PRIMARY KEY (id),
  CONSTRAINT "UC_genre__name" UNIQUE (name)
)
WITH (
  OIDS=FALSE
);

ALTER TABLE genre
  OWNER TO postgres;
COMMENT ON TABLE genre
  IS 'UPDATE genre set is_movie_genre = true where name in (
''Action'',''Comedy'',
''Fantasy'',''Musical'',
''Short'',''Adventure'',
''Crime'',''Family'',
''Mystery'',''Thriller'',
''Adult'',''Documentary'',
''Film-Noir'',''Romance'',
''War'',''Animation'',
''Drama'',''Horror'',
''Sci-Fi'',''Western'',
''Sport''
)
';

-- Index: "IX_genre__id"

DROP INDEX IF EXISTS "IX_genre__id";

CREATE UNIQUE INDEX "IX_genre__id"
  ON genre
  USING btree
  (id);

-- Index: "IX_genre__name"

DROP INDEX IF EXISTS "IX_genre__name";

CREATE UNIQUE INDEX "IX_genre__name"
  ON genre
  USING btree
  (name COLLATE pg_catalog."default");
ALTER TABLE genre CLUSTER ON "IX_genre__name";


-- Table: public.actor

DROP TABLE IF EXISTS public.actor CASCADE;

-- Sequence: public.actor_id_seq

DROP SEQUENCE IF EXISTS public.actor_id_seq;

CREATE SEQUENCE public.actor_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 993
  CACHE 1;
ALTER TABLE public.actor_id_seq
  OWNER TO postgres;


CREATE TABLE public.actor
(
  id integer NOT NULL DEFAULT nextval('actor_id_seq'::regclass),
  name text,
  gender "char",
  fname_id integer,
  lname_id integer,
  name_index smallint,
  CONSTRAINT actor_id PRIMARY KEY (id),
  CONSTRAINT "FK_actor__fname_id" FOREIGN KEY (fname_id)
      REFERENCES public.actor_name (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_actor__lname_id" FOREIGN KEY (lname_id)
      REFERENCES public.actor_name (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "UC_actor__name__gender" UNIQUE (name, gender)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.actor
  OWNER TO postgres;

-- Index: public."FKI_actor__fname_id"

DROP INDEX IF EXISTS public."FKI_actor__fname_id";

CREATE INDEX "FKI_actor__fname_id"
  ON public.actor
  USING btree
  (fname_id);

-- Index: public."FKI_actor__lname_id"

DROP INDEX IF EXISTS public."FKI_actor__lname_id";

CREATE INDEX "FKI_actor__lname_id"
  ON public.actor
  USING btree
  (lname_id);

-- Index: public."IX_actor__id"

DROP INDEX IF EXISTS public."IX_actor__id";

CREATE UNIQUE INDEX "IX_actor__id"
  ON public.actor
  USING btree
  (id);
ALTER TABLE public.actor CLUSTER ON "IX_actor__id";

-- Index: public."IX_actor__name__gender"

DROP INDEX IF EXISTS public."IX_actor__name__gender";

CREATE UNIQUE INDEX "IX_actor__name__gender"
  ON public.actor
  USING btree
  (name COLLATE pg_catalog."default", gender);


-- Table: public.actor_name

DROP TABLE IF EXISTS public.actor_name CASCADE;

-- Sequence: public.actor_name_id_seq

DROP SEQUENCE IF EXISTS public.actor_name_id_seq;

CREATE SEQUENCE public.actor_name_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1464
  CACHE 1;
ALTER TABLE public.actor_name_id_seq
  OWNER TO postgres;

CREATE TABLE public.actor_name
(
  id integer NOT NULL DEFAULT nextval('actor_name_id_seq'::regclass),
  name text NOT NULL,
  CONSTRAINT "PK_actor_name__id" PRIMARY KEY (id),
  CONSTRAINT "UC_actor_name__name" UNIQUE (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.actor_name
  OWNER TO postgres;

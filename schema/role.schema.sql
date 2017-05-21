-- Table: public.role

DROP TABLE IF EXISTS public.role CASCADE;

-- Sequence: public.role_id_seq

DROP SEQUENCE IF EXISTS public.role_id_seq;

CREATE SEQUENCE public.role_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 59637
  CACHE 1;
ALTER TABLE public.role_id_seq
  OWNER TO postgres;

CREATE TABLE public.role
(
  id integer NOT NULL DEFAULT nextval('role_id_seq'::regclass),
  name text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.role
  OWNER TO postgres;

-- Table: role

DROP TABLE IF EXISTS role CASCADE;

-- Sequence: role_id_seq

DROP SEQUENCE IF EXISTS role_id_seq;

CREATE SEQUENCE role_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 59637
  CACHE 1;
ALTER TABLE role_id_seq
  OWNER TO postgres;

CREATE TABLE role
(
  id integer NOT NULL DEFAULT nextval('role_id_seq'::regclass),
  name text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE role
  OWNER TO postgres;

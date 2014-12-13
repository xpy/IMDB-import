--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: light; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA light;


ALTER SCHEMA light OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgres_fdw; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgres_fdw WITH SCHEMA public;


--
-- Name: EXTENSION postgres_fdw; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgres_fdw IS 'foreign-data wrapper for remote PostgreSQL servers';


SET search_path = light, pg_catalog;

--
-- Name: CT_movie__actor_to_movie; Type: TYPE; Schema: light; Owner: postgres
--

CREATE TYPE "CT_movie__actor_to_movie" AS (
	id integer,
	name text,
	year integer,
	year_id text,
	rating double precision,
	votes integer,
	billing_position integer,
	roles text
);


ALTER TYPE light."CT_movie__actor_to_movie" OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: CT_movie__actor_to_movie; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE "CT_movie__actor_to_movie" AS (
	id integer,
	name text,
	year integer,
	year_id text,
	rating double precision,
	votes integer,
	billing_position integer,
	roles text
);


ALTER TYPE public."CT_movie__actor_to_movie" OWNER TO postgres;

SET search_path = light, pg_catalog;

--
-- Name: CF_get_actor_genre_rating(integer); Type: FUNCTION; Schema: light; Owner: postgres
--

CREATE FUNCTION "CF_get_actor_genre_rating"(_actor_id integer) RETURNS TABLE(name text, rating double precision, cnt bigint)
    LANGUAGE sql
    AS $$SELECT 
genre.name,
SUM(rating)/COUNT(genre.name) rating,
COUNT(genre.name) cnt 
FROM 
genre 
JOIN 
genre_to_movie on genre.id = genre_id 
JOIN 
movie on movie.id = genre_to_movie.movie_id 
JOIN 
actor_to_movie on movie.id = actor_to_movie.movie_id 
JOIN 
actor on actor.id = actor_to_movie.actor_id 
WHERE 
actor_id = _actor_id
AND 
rating IS NOT NULL
GROUP BY genre.name$$;


ALTER FUNCTION light."CF_get_actor_genre_rating"(_actor_id integer) OWNER TO postgres;

--
-- Name: CF_get_actor_movies(integer); Type: FUNCTION; Schema: light; Owner: postgres
--

CREATE FUNCTION "CF_get_actor_movies"(_actor_id integer) RETURNS TABLE(id integer, name text, year integer, year_id text, rating double precision, votes integer, billing_position integer, roles text)
    LANGUAGE sql
    AS $$SELECT 
movie.id id,
name,
year ,
year_id,
rating,
votes,
billing_position,
roles 
FROM 
movie JOIN actor_to_movie 
on 
movie.id = movie_id 
WHERE 
actor_id = _actor_id 

$$;


ALTER FUNCTION light."CF_get_actor_movies"(_actor_id integer) OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: CF_get_actor_genre_rating(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION "CF_get_actor_genre_rating"(_actor_id integer) RETURNS TABLE(name text, rating double precision, cnt bigint)
    LANGUAGE sql
    AS $$SELECT 
genre.name,
SUM(rating)/COUNT(genre.name) rating,
COUNT(genre.name) cnt 
FROM 
genre 
JOIN 
genre_to_movie on genre.id = genre_id 
JOIN 
movie on movie.id = genre_to_movie.movie_id 
JOIN 
actor_to_movie on movie.id = actor_to_movie.movie_id 
JOIN 
actor on actor.id = actor_to_movie.actor_id 
WHERE 
actor_id = _actor_id
AND 
rating IS NOT NULL
GROUP BY genre.name$$;


ALTER FUNCTION public."CF_get_actor_genre_rating"(_actor_id integer) OWNER TO postgres;

--
-- Name: CF_get_actor_movies(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION "CF_get_actor_movies"(_actor_id integer) RETURNS TABLE(id integer, name text, year integer, year_id text, rating double precision, votes integer, billing_position integer, roles text)
    LANGUAGE sql
    AS $$SELECT 
movie.id id,
name,
year ,
year_id,
rating,
votes,
billing_position,
roles 
FROM 
movie JOIN actor_to_movie 
on 
movie.id = movie_id 
WHERE 
actor_id = _actor_id 

$$;


ALTER FUNCTION public."CF_get_actor_movies"(_actor_id integer) OWNER TO postgres;

--
-- Name: r_imdb_light; Type: SERVER; Schema: -; Owner: postgres
--

CREATE SERVER r_imdb_light FOREIGN DATA WRAPPER postgres_fdw OPTIONS (
    dbname 'IMDB_light',
    host 'postgres',
    port '5432'
);


ALTER SERVER r_imdb_light OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE genre (
    id smallint NOT NULL,
    name text,
    is_movie_genre boolean
);


ALTER TABLE public.genre OWNER TO postgres;

--
-- Name: TABLE genre; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE genre IS 'UPDATE genre set is_movie_genre = true where name in (
''Action'',''Comedy'',
''Fantasy'',''Musical'',
''Short'',''Adventure'',
''Crime'',''Family'',
''Mystery'',''Thriller'',
''Adult'',''Documentary'',
''Film-Noir'',''Romance'',
''War'',''Animation'',
''Drama'',''Horror'',
''Sci-Fi'',''Western''
)
';


--
-- Name: genre_to_movie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE genre_to_movie (
    id integer NOT NULL,
    genre_id integer,
    movie_id integer
);


ALTER TABLE public.genre_to_movie OWNER TO postgres;

--
-- Name: movie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movie (
    id integer NOT NULL,
    name text,
    year integer,
    year_id text,
    rating double precision,
    votes integer
);


ALTER TABLE public.movie OWNER TO postgres;

SET search_path = light, pg_catalog;

--
-- Name: VW_movie; Type: VIEW; Schema: light; Owner: postgres
--

CREATE VIEW "VW_movie" AS
 SELECT DISTINCT movie.id,
    movie.name,
    movie.year,
    movie.year_id,
    movie.rating,
    movie.votes
   FROM public.movie
  WHERE (NOT (EXISTS ( SELECT 1
           FROM public.genre_to_movie
          WHERE ((genre_to_movie.movie_id = movie.id) AND (genre_to_movie.genre_id IN ( SELECT genre.id
                   FROM public.genre
                  WHERE (genre.is_movie_genre = false)))))));


ALTER TABLE light."VW_movie" OWNER TO postgres;

--
-- Name: actor; Type: TABLE; Schema: light; Owner: postgres; Tablespace: 
--

CREATE TABLE actor (
    id integer NOT NULL,
    name text,
    gender "char"
);


ALTER TABLE light.actor OWNER TO postgres;

--
-- Name: actor_name; Type: TABLE; Schema: light; Owner: postgres; Tablespace: 
--

CREATE TABLE actor_name (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE light.actor_name OWNER TO postgres;

--
-- Name: actor_name_id_seq; Type: SEQUENCE; Schema: light; Owner: postgres
--

CREATE SEQUENCE actor_name_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE light.actor_name_id_seq OWNER TO postgres;

--
-- Name: actor_name_id_seq; Type: SEQUENCE OWNED BY; Schema: light; Owner: postgres
--

ALTER SEQUENCE actor_name_id_seq OWNED BY actor_name.id;


--
-- Name: actor_to_movie; Type: TABLE; Schema: light; Owner: postgres; Tablespace: 
--

CREATE TABLE actor_to_movie (
    id integer NOT NULL,
    actor_id integer,
    movie_id integer,
    billing_position integer,
    roles text
);


ALTER TABLE light.actor_to_movie OWNER TO postgres;

--
-- Name: actor_to_movie_id_seq; Type: SEQUENCE; Schema: light; Owner: postgres
--

CREATE SEQUENCE actor_to_movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE light.actor_to_movie_id_seq OWNER TO postgres;

--
-- Name: actor_to_movie_id_seq; Type: SEQUENCE OWNED BY; Schema: light; Owner: postgres
--

ALTER SEQUENCE actor_to_movie_id_seq OWNED BY actor_to_movie.id;


--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: light; Owner: postgres
--

CREATE SEQUENCE actors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE light.actors_id_seq OWNER TO postgres;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: light; Owner: postgres
--

ALTER SEQUENCE actors_id_seq OWNED BY actor.id;


--
-- Name: genre; Type: TABLE; Schema: light; Owner: postgres; Tablespace: 
--

CREATE TABLE genre (
    id smallint NOT NULL,
    name text,
    is_movie_genre boolean
);


ALTER TABLE light.genre OWNER TO postgres;

--
-- Name: TABLE genre; Type: COMMENT; Schema: light; Owner: postgres
--

COMMENT ON TABLE genre IS 'UPDATE genre set is_movie_genre = true where name in (
''Action'',''Comedy'',
''Fantasy'',''Musical'',
''Short'',''Adventure'',
''Crime'',''Family'',
''Mystery'',''Thriller'',
''Adult'',''Documentary'',
''Film-Noir'',''Romance'',
''War'',''Animation'',
''Drama'',''Horror'',
''Sci-Fi'',''Western''
)
';


--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: light; Owner: postgres
--

CREATE SEQUENCE genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE light.genre_id_seq OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: light; Owner: postgres
--

ALTER SEQUENCE genre_id_seq OWNED BY genre.id;


--
-- Name: genre_to_movie; Type: TABLE; Schema: light; Owner: postgres; Tablespace: 
--

CREATE TABLE genre_to_movie (
    id integer NOT NULL,
    genre_id integer,
    movie_id integer
);


ALTER TABLE light.genre_to_movie OWNER TO postgres;

--
-- Name: genre_to_movie_id_seq; Type: SEQUENCE; Schema: light; Owner: postgres
--

CREATE SEQUENCE genre_to_movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE light.genre_to_movie_id_seq OWNER TO postgres;

--
-- Name: genre_to_movie_id_seq; Type: SEQUENCE OWNED BY; Schema: light; Owner: postgres
--

ALTER SEQUENCE genre_to_movie_id_seq OWNED BY genre_to_movie.id;


--
-- Name: movie; Type: TABLE; Schema: light; Owner: postgres; Tablespace: 
--

CREATE TABLE movie (
    id integer NOT NULL,
    name text,
    year integer,
    year_id text,
    rating double precision,
    votes integer
);


ALTER TABLE light.movie OWNER TO postgres;

--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: light; Owner: postgres
--

CREATE SEQUENCE movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE light.movie_id_seq OWNER TO postgres;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: light; Owner: postgres
--

ALTER SEQUENCE movie_id_seq OWNED BY movie.id;


SET search_path = public, pg_catalog;

--
-- Name: VW_movie; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW "VW_movie" AS
 SELECT DISTINCT movie.id,
    movie.name,
    movie.year,
    movie.year_id,
    movie.rating,
    movie.votes
   FROM movie
  WHERE (NOT (EXISTS ( SELECT 1
           FROM genre_to_movie
          WHERE ((genre_to_movie.movie_id = movie.id) AND (genre_to_movie.genre_id IN ( SELECT genre.id
                   FROM genre
                  WHERE (genre.is_movie_genre = false)))))));


ALTER TABLE public."VW_movie" OWNER TO postgres;

--
-- Name: actor; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actor (
    id integer NOT NULL,
    name text,
    gender "char"
);


ALTER TABLE public.actor OWNER TO postgres;

--
-- Name: actor_name; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actor_name (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.actor_name OWNER TO postgres;

--
-- Name: actor_name_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actor_name_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_name_id_seq OWNER TO postgres;

--
-- Name: actor_name_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actor_name_id_seq OWNED BY actor_name.id;


--
-- Name: actor_to_movie; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE actor_to_movie (
    id integer NOT NULL,
    actor_id integer,
    movie_id integer,
    billing_position integer,
    roles text
);


ALTER TABLE public.actor_to_movie OWNER TO postgres;

--
-- Name: actor_to_movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actor_to_movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_to_movie_id_seq OWNER TO postgres;

--
-- Name: actor_to_movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actor_to_movie_id_seq OWNED BY actor_to_movie.id;


--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE actors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO postgres;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE actors_id_seq OWNED BY actor.id;


--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genre_id_seq OWNER TO postgres;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE genre_id_seq OWNED BY genre.id;


--
-- Name: genre_to_movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE genre_to_movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genre_to_movie_id_seq OWNER TO postgres;

--
-- Name: genre_to_movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE genre_to_movie_id_seq OWNED BY genre_to_movie.id;


--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE movie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_id_seq OWNER TO postgres;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE movie_id_seq OWNED BY movie.id;


SET search_path = light, pg_catalog;

--
-- Name: id; Type: DEFAULT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY actor ALTER COLUMN id SET DEFAULT nextval('actors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY actor_name ALTER COLUMN id SET DEFAULT nextval('actor_name_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY actor_to_movie ALTER COLUMN id SET DEFAULT nextval('actor_to_movie_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY genre ALTER COLUMN id SET DEFAULT nextval('genre_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY genre_to_movie ALTER COLUMN id SET DEFAULT nextval('genre_to_movie_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY movie ALTER COLUMN id SET DEFAULT nextval('movie_id_seq'::regclass);


SET search_path = public, pg_catalog;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actor ALTER COLUMN id SET DEFAULT nextval('actors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actor_name ALTER COLUMN id SET DEFAULT nextval('actor_name_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actor_to_movie ALTER COLUMN id SET DEFAULT nextval('actor_to_movie_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genre ALTER COLUMN id SET DEFAULT nextval('genre_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genre_to_movie ALTER COLUMN id SET DEFAULT nextval('genre_to_movie_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY movie ALTER COLUMN id SET DEFAULT nextval('movie_id_seq'::regclass);


SET search_path = light, pg_catalog;

--
-- Name: PK_actor_name__id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_name
    ADD CONSTRAINT "PK_actor_name__id" PRIMARY KEY (id);


--
-- Name: PK_actor_to_movie__id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "PK_actor_to_movie__id" PRIMARY KEY (id);


--
-- Name: PK_genre__id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT "PK_genre__id" PRIMARY KEY (id);


--
-- Name: PK_genre_to_movie__id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genre_to_movie
    ADD CONSTRAINT "PK_genre_to_movie__id" PRIMARY KEY (id);


--
-- Name: UC_actor__name__gender; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor
    ADD CONSTRAINT "UC_actor__name__gender" UNIQUE (name, gender);


--
-- Name: UC_actor_name__name; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_name
    ADD CONSTRAINT "UC_actor_name__name" UNIQUE (name);


--
-- Name: UC_actor_to_movie__actor_id__movie_id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "UC_actor_to_movie__actor_id__movie_id" UNIQUE (actor_id, movie_id);


--
-- Name: UC_genre__name; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT "UC_genre__name" UNIQUE (name);


--
-- Name: UC_movie__name__year_id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movie
    ADD CONSTRAINT "UC_movie__name__year_id" UNIQUE (name, year_id);


--
-- Name: actor_id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor
    ADD CONSTRAINT actor_id PRIMARY KEY (id);


--
-- Name: movie_id; Type: CONSTRAINT; Schema: light; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movie
    ADD CONSTRAINT movie_id PRIMARY KEY (id);


SET search_path = public, pg_catalog;

--
-- Name: PK_actor_name__id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_name
    ADD CONSTRAINT "PK_actor_name__id" PRIMARY KEY (id);


--
-- Name: PK_actor_to_movie__id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "PK_actor_to_movie__id" PRIMARY KEY (id);


--
-- Name: PK_genre__id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT "PK_genre__id" PRIMARY KEY (id);


--
-- Name: PK_genre_to_movie__id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genre_to_movie
    ADD CONSTRAINT "PK_genre_to_movie__id" PRIMARY KEY (id);


--
-- Name: UC_actor__name__gender; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor
    ADD CONSTRAINT "UC_actor__name__gender" UNIQUE (name, gender);


--
-- Name: UC_actor_name__name; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_name
    ADD CONSTRAINT "UC_actor_name__name" UNIQUE (name);


--
-- Name: UC_actor_to_movie__actor_id__movie_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "UC_actor_to_movie__actor_id__movie_id" UNIQUE (actor_id, movie_id);


--
-- Name: UC_genre__name; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT "UC_genre__name" UNIQUE (name);


--
-- Name: UC_movie__name__year_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movie
    ADD CONSTRAINT "UC_movie__name__year_id" UNIQUE (name, year_id);


--
-- Name: actor_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY actor
    ADD CONSTRAINT actor_id PRIMARY KEY (id);


--
-- Name: movie_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY movie
    ADD CONSTRAINT movie_id PRIMARY KEY (id);


SET search_path = light, pg_catalog;

--
-- Name: IX_actor__id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_actor__id" ON actor USING btree (id);

ALTER TABLE actor CLUSTER ON "IX_actor__id";


--
-- Name: IX_actor__name__gender; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_actor__name__gender" ON actor USING btree (name, gender);


--
-- Name: IX_actor_to_movie__actor_id__movie_id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_actor_to_movie__actor_id__movie_id" ON actor_to_movie USING btree (actor_id, movie_id);

ALTER TABLE actor_to_movie CLUSTER ON "IX_actor_to_movie__actor_id__movie_id";


--
-- Name: IX_genre__id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre__id" ON genre USING btree (id);


--
-- Name: IX_genre__name; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre__name" ON genre USING btree (name);

ALTER TABLE genre CLUSTER ON "IX_genre__name";


--
-- Name: IX_genre_to_movie__genre_id__movie_id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre_to_movie__genre_id__movie_id" ON genre_to_movie USING btree (genre_id, movie_id);

ALTER TABLE genre_to_movie CLUSTER ON "IX_genre_to_movie__genre_id__movie_id";


--
-- Name: IX_genre_to_movie__id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre_to_movie__id" ON genre_to_movie USING btree (id);


--
-- Name: IX_movie__id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_movie__id" ON movie USING btree (id);

ALTER TABLE movie CLUSTER ON "IX_movie__id";


--
-- Name: IX_movie__name__year_id; Type: INDEX; Schema: light; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_movie__name__year_id" ON movie USING btree (name, year_id);


SET search_path = public, pg_catalog;

--
-- Name: IX_actor__id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_actor__id" ON actor USING btree (id);

ALTER TABLE actor CLUSTER ON "IX_actor__id";


--
-- Name: IX_actor__name__gender; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_actor__name__gender" ON actor USING btree (name, gender);


--
-- Name: IX_actor_to_movie__actor_id__movie_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_actor_to_movie__actor_id__movie_id" ON actor_to_movie USING btree (actor_id, movie_id);

ALTER TABLE actor_to_movie CLUSTER ON "IX_actor_to_movie__actor_id__movie_id";


--
-- Name: IX_genre__id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre__id" ON genre USING btree (id);


--
-- Name: IX_genre__name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre__name" ON genre USING btree (name);

ALTER TABLE genre CLUSTER ON "IX_genre__name";


--
-- Name: IX_genre_to_movie__genre_id__movie_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre_to_movie__genre_id__movie_id" ON genre_to_movie USING btree (genre_id, movie_id);

ALTER TABLE genre_to_movie CLUSTER ON "IX_genre_to_movie__genre_id__movie_id";


--
-- Name: IX_genre_to_movie__id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_genre_to_movie__id" ON genre_to_movie USING btree (id);


--
-- Name: IX_movie__id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_movie__id" ON movie USING btree (id);

ALTER TABLE movie CLUSTER ON "IX_movie__id";


--
-- Name: IX_movie__name__year_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE UNIQUE INDEX "IX_movie__name__year_id" ON movie USING btree (name, year_id);


SET search_path = light, pg_catalog;

--
-- Name: RL_movie__insert_duplicate; Type: RULE; Schema: light; Owner: postgres
--

CREATE RULE "RL_movie__insert_duplicate" AS
    ON INSERT TO movie
   WHERE (EXISTS ( SELECT 1
           FROM movie
          WHERE ((movie.name = new.name) AND (movie.year_id = new.year_id)))) DO INSTEAD NOTHING;
ALTER TABLE movie DISABLE RULE "RL_movie__insert_duplicate";


SET search_path = public, pg_catalog;

--
-- Name: RL_movie__insert_duplicate; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE "RL_movie__insert_duplicate" AS
    ON INSERT TO movie
   WHERE (EXISTS ( SELECT 1
           FROM movie
          WHERE ((movie.name = new.name) AND (movie.year_id = new.year_id)))) DO INSTEAD NOTHING;
ALTER TABLE movie DISABLE RULE "RL_movie__insert_duplicate";


SET search_path = light, pg_catalog;

--
-- Name: FK_actor_to_movie__actor_id; Type: FK CONSTRAINT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "FK_actor_to_movie__actor_id" FOREIGN KEY (actor_id) REFERENCES actor(id) ON DELETE CASCADE;


--
-- Name: FK_actor_to_movie__movie_id; Type: FK CONSTRAINT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "FK_actor_to_movie__movie_id" FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE;


--
-- Name: FK_genre_to_movie__genre; Type: FK CONSTRAINT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY genre_to_movie
    ADD CONSTRAINT "FK_genre_to_movie__genre" FOREIGN KEY (genre_id) REFERENCES genre(id) ON DELETE CASCADE;


--
-- Name: FK_genre_to_movie__movie_id; Type: FK CONSTRAINT; Schema: light; Owner: postgres
--

ALTER TABLE ONLY genre_to_movie
    ADD CONSTRAINT "FK_genre_to_movie__movie_id" FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE;


SET search_path = public, pg_catalog;

--
-- Name: FK_actor_to_movie__actor_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "FK_actor_to_movie__actor_id" FOREIGN KEY (actor_id) REFERENCES actor(id) ON DELETE CASCADE;


--
-- Name: FK_actor_to_movie__movie_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY actor_to_movie
    ADD CONSTRAINT "FK_actor_to_movie__movie_id" FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE;


--
-- Name: FK_genre_to_movie__genre; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genre_to_movie
    ADD CONSTRAINT "FK_genre_to_movie__genre" FOREIGN KEY (genre_id) REFERENCES genre(id) ON DELETE CASCADE;


--
-- Name: FK_genre_to_movie__movie_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genre_to_movie
    ADD CONSTRAINT "FK_genre_to_movie__movie_id" FOREIGN KEY (movie_id) REFERENCES movie(id) ON DELETE CASCADE;


--
-- Name: light; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA light FROM PUBLIC;
REVOKE ALL ON SCHEMA light FROM postgres;
GRANT ALL ON SCHEMA light TO postgres;
GRANT ALL ON SCHEMA light TO PUBLIC;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


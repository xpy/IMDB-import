-- Function: "CF_get_actor_movies"(integer)

DROP FUNCTION IF EXISTS "CF_get_actor_movies"(integer);

CREATE OR REPLACE FUNCTION "CF_get_actor_movies"(IN _actor_id integer)
  RETURNS TABLE(id integer, name text, year integer, year_id smallint, rating double precision, votes integer, billing_position integer, roles text) AS
$BODY$SELECT
movie.id id,
name,
year,
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

$BODY$
  LANGUAGE sql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION "CF_get_actor_movies"(integer)
  OWNER TO postgres;

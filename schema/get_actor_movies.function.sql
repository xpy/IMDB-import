-- Function: "CF_get_actor_movies"(integer)

DROP FUNCTION IF EXISTS "CF_get_actor_movies"(integer);

CREATE OR REPLACE FUNCTION "CF_get_actor_movies"(IN _actor_id integer)
  RETURNS TABLE(id integer, name text, year integer, rating double precision, votes integer, billing_position integer, role text) AS
$BODY$SELECT
movie.id id,
movie.name,
year,
rating,
votes,
billing_position,
role.name
FROM
movie JOIN actor_to_movie
ON
movie.id = movie_id
JOIN role
ON role.id = actor_to_movie.role_id
WHERE
actor_id = _actor_id

$BODY$
  LANGUAGE sql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION "CF_get_actor_movies"(integer)
  OWNER TO postgres;

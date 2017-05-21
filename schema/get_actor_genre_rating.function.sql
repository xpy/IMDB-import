-- Function: "CF_get_actor_genre_rating"(integer)

DROP FUNCTION IF EXISTS "CF_get_actor_genre_rating"(integer);

CREATE OR REPLACE FUNCTION "CF_get_actor_genre_rating"(IN _actor_id integer)
  RETURNS TABLE(name text, rating double precision, cnt bigint) AS
$BODY$SELECT
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
GROUP BY genre.name$BODY$
  LANGUAGE sql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION "CF_get_actor_genre_rating"(integer)
  OWNER TO postgres;

DO $$
DECLARE _votes integer;
DECLARE _actor_movies integer;

BEGIN
_votes := 100000;
_actor_movies := 6;

/*
CREATE UNLOGGED TABLE tmp_movie (
  id serial NOT NULL,
  name text,
  year integer,
  year_id text,
  rating double precision,
  votes integer,
);
*/

TRUNCATE  TABLE light.movie CASCADE;

INSERT INTO light.movie 
(
id,
  name,
  year,
  year_id,
  rating,
  votes
  )
SELECT 
 id,
  name,
  year,
  year_id,
  rating,
  votes
 FROM public."VW_movie" WHERE rating is not null and votes > _votes;

--RAISE NOTICE 'Movies completed';

/* ****************************** */ 
/* ******** INSERT actor ******** */
/* ****************************** */ 

TRUNCATE  TABLE light.actor CASCADE;

INSERT INTO light.actor (id,name,gender)
SELECT id,name,gender FROM public.actor WHERE id in (
SELECT id FROM (
select actor.id,count(actor_to_movie.*) cnt 
from 
public.actor actor
JOIN 
public.actor_to_movie actor_to_movie
on 
actor.id= actor_id 
JOIN 
light.movie movie 
on 
movie.id = movie_id 
WHERE 
rating is not null
and votes > _votes 
group by actor.id 
ORDER by cnt desc -- limit 10
)a where cnt >= _actor_movies );

TRUNCATE  TABLE light.actor_to_movie;

INSERT INTO light.actor_to_movie (id,actor_id,movie_id,billing_position,roles)
SELECT DISTINCT actor_to_movie.id,actor_to_movie.actor_id,actor_to_movie.movie_id,actor_to_movie.billing_position,actor_to_movie.roles 
FROM light.actor actor JOIN public.actor_to_movie actor_to_movie ON actor.id = actor_id JOIN light.movie movie on movie.id = movie_id;

TRUNCATE TABLE light.genre CASCADE;
INSERT INTO light.genre (id,name,is_movie_genre) SELECT id,name,is_movie_genre FROM public.genre WHERE public.genre.is_movie_genre = true;

TRUNCATE TABLE light.genre_to_movie;
INSERT INTO light.genre_to_movie (id,movie_id,genre_id) SELECT g.id,g.movie_id,g.genre_id FROM public.genre_to_movie g JOIN light.movie m ON movie_id =m.id order by genre_id;

END $$


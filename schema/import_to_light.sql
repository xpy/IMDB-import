DO $$ DECLARE _votes integer;

BEGIN
_votes := 1000;


-- INSERT ACTOR NAMES
TRUNCATE  TABLE light.actor_name CASCADE;
INSERT INTO light.actor_name (id,name)
SELECT id,name FROM public.actor_name;

-- INSERT ACTORS
TRUNCATE  TABLE light.actor CASCADE;

INSERT INTO light.actor (id, gender, fname_id, lname_id, name_index)
SELECT id, gender, fname_id, lname_id, name_index FROM public.actor;

-- INSERT MOVIES
TRUNCATE  TABLE light.movie CASCADE;

INSERT INTO light.movie
(id,name,year,year_id,rating,votes)
SELECT id, name, year, year_id, rating, votes
FROM public."VW_movie" movie WHERE movie.rating is not null and movie.votes > _votes
AND movie.id in (
    SELECT movie_id FROM public.actor_to_movie
    JOIN public.role ON role_id = role.id AND (role.name NOT LIKE 'Himself%' AND role.name NOT LIKE 'Herself%'
    AND role.name NOT LIKE 'Narator' AND role.name NOT LIKE 'Narrator'
    )
    WHERE actor_id IN
    (
        SELECT id from public.actor
    )
    AND billing_position IS NOT NULL

);

-- INSERT ROLES
TRUNCATE  TABLE light.role;

INSERT INTO light.role (id,name)
SELECT DISTINCT role.id,role.name FROM public.role JOIN public.actor_to_movie
ON actor_to_movie.role_id = role.id JOIN light.movie ON actor_to_movie.movie_id = movie.id;

-- INSERT ACTOR TO MOVIE
--TRUNCATE TABLE light.actor_to_movie;

INSERT INTO light.actor_to_movie (id,actor_id,movie_id,billing_position,roles,role_id)
SELECT DISTINCT actor_to_movie.id,actor_to_movie.actor_id,actor_to_movie.movie_id,actor_to_movie.billing_position,actor_to_movie.roles,actor_to_movie.role_id
FROM
light.actor actor
    JOIN public.actor_to_movie actor_to_movie ON actor.id = actor_id
    JOIN light.movie movie on movie.id = movie_id
WHERE billing_position IS NOT NULL;

-- INSERT GENRES
TRUNCATE TABLE light.genre CASCADE;

INSERT INTO light.genre (id,name,is_movie_genre) SELECT id,name,is_movie_genre FROM genre WHERE genre.is_movie_genre = true;

-- INSERT GENRE TO MOVIE
--TRUNCATE TABLE light.genre_to_movie;

INSERT INTO light.genre_to_movie (id,movie_id,genre_id)
SELECT g.id,g.movie_id,g.genre_id
FROM genre_to_movie g JOIN light.movie m ON movie_id =m.id order by genre_id;

END $$;;

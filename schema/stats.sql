 
 select count(*) from "VW_movie" where rating is not null and votes > 100 --60753
 select count(*) from "VW_movie" where rating is not null and votes > 500 --23598
 select count(*) from "VW_movie" where rating is not null and votes > 1000 --15322
 select count(*) from "VW_movie" where rating is not null and votes > 2500 --8645
 select count(*) from "VW_movie" where rating is not null and votes > 5000 --5537
 select count(*) from "VW_movie" where rating is not null and votes > 10000 --3629
 select count(*) from "VW_movie" where rating is not null and votes > 20000 --2347
 select count(*) from "VW_movie" where rating is not null and votes > 50000 --1192
 select count(*) from "VW_movie" where rating is not null and votes > 80000 --748
 select count(*) from "VW_movie" where rating is not null and votes > 100000 --570
 select count(*) from "VW_movie" --where rating is not null and votes > 100 -- 671421


select actor.id,fname.name,lname.name,
count(actor_to_movie.*) cnt
from
actor
JOIN
actor_to_movie
on
actor.id= actor_id
JOIN
"VW_movie" movie
on
movie.id = movie_id
JOIN
actor_name fname
ON fname.id = actor.fname_id
JOIN
actor_name lname
ON lname.id = actor.lname_id

WHERE
rating is not null
and movie.id in (select movie_id from genre where genre.id in (select id from genre where is_movie_genre = true))
and votes > 50
group by actor.id,fname.name,lname.name
ORDER by cnt desc -- limit 10


select movie.*,genre.name from movie
JOIN genre_to_movie on movie.id = genre_to_movie.movie_id
JOIN genre on genre.id = genre_to_movie.genre_id
 where movie.id in (select movie_id from actor_to_movie where actor_id =359)
 and genre.is_movie_genre = true

--delete from actor_to_movie
select * from movie where name = '100 Years of Horror'
select * from ragin
select * from actor limit 100
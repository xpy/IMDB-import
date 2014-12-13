 
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


select actor.name,count(actor_to_movie.*) cnt 
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
WHERE 
rating is not null
and votes > 50000 
group by actor.name 
ORDER by cnt desc -- limit 10

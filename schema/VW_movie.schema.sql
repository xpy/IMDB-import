-- View: "VW_movie"

DROP VIEW IF EXISTS "VW_movie";

CREATE OR REPLACE VIEW "VW_movie" AS
 SELECT DISTINCT movie.id,
    movie.name,
    movie.year,
    movie.year_id,
    movie.rating,
    movie.votes
   FROM movie
  WHERE NOT (EXISTS ( SELECT 1
           FROM genre_to_movie
             JOIN genre ON genre.id = genre_to_movie.genre_id
          WHERE movie.id = genre_to_movie.movie_id AND genre.is_movie_genre = false)) AND (EXISTS ( SELECT 1
           FROM genre_to_movie
             JOIN genre ON genre.id = genre_to_movie.genre_id
          WHERE movie.id = genre_to_movie.movie_id AND genre.is_movie_genre = true));

ALTER TABLE "VW_movie"
  OWNER TO postgres;

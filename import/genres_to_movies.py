import psycopg2
import sys

import re
import variables
import functions
import codecs


class GenresToMoviesImport:
    fileName = 'genres.list'
    f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
    cur = None
    conn = None

    @classmethod
    def insert_genre_to_movie(cls, genre, movie):
        try:
            cls.cur.execute("INSERT INTO genre_to_movie (genre_id,movie_id) "
                            "SELECT genre.id,movie.id from genre,movie "
                            "where genre.name = %s and movie.name = %s and movie.year_id = %s and movie.year = %s  "
                            # "AND NOT EXISTS ( SELECT 1 FROM genre_to_movie where genre_id = genre.id and movie_id = movie.id)"
                            ,
                            (genre, movie['name'], movie['year_id'], movie['year']))
        except psycopg2.IntegrityError:
            print(sys.exc_info())
            print("XESTHKA ( nomizw )", movie, genre)

    @classmethod
    def add_genres_to_movies(cls):
        i = 1
        line = functions.read_file_line(cls.f).split('\t')
        prev_movie = {'name': None, 'year_id': None}
        prev_genre = None
        prev_movie_string = None
        while line[0] != '':
            movie_string = line[0]
            if re.match('.*{.*\}$', movie_string) is None:
                movie = prev_movie if movie_string == prev_movie_string else functions.get_movie_split(movie_string)
                genre = line[-1].replace('\n', '')
                # print(movie, genre, i)
                if i % 10000 == 0:
                    print(movie, genre, i)
                if movie != prev_movie or genre != prev_genre:
                    cls.insert_genre_to_movie(genre, movie)
                    cls.conn.commit()
                    i += 1
                    prev_movie = movie
                    prev_genre = genre
            prev_movie_string = movie_string
            line = functions.read_file_line(cls.f).split('\t')

    @classmethod
    def run(cls):
        functions.jump_to_line_with_string(cls.f, '8: THE GENRES LIST')
        functions.jump_lines(cls.f, 2)

        cls.conn = psycopg2.connect(variables.postgres_credentials)
        cls.cur = cls.conn.cursor()

        functions.reset_table(cls.cur, 'genre_to_movie')

        cls.cur.execute("SET transform_null_equals TO ON")
        cls.cur.execute("CREATE TEMP TABLE tmp_genre_to_movie"
                        "(genre_id int,movie_id int);")

        functions.start_timer('Add genres to movies')
        cls.add_genres_to_movies()
        functions.check_timer('Add genres to movies')

        functions.start_timer('Commit to DB')
        cls.conn.commit()
        functions.check_timer('Commit to DB')

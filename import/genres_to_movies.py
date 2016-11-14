import psycopg2
import variables
import functions
import codecs

fileName = 'genres.list'
f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')


def insert_genre_to_movie(genre, movie):
    # print( genre, movie)
    cur.execute("INSERT INTO genre_to_movie (genre_id,movie_id) "
                "SELECT genre.id,movie.id from genre,movie "
                "where genre.name = %s and movie.name = %s and movie.year_id = %s  and movie.year = %s  "
                "AND NOT EXISTS ( SELECT 1 FROM genre_to_movie where genre_id = genre.id and movie_id = movie.id)"
                ,
                [genre, movie['name'], movie['year_id'], movie['year']])


def add_genres_to_movies():
    i = 0
    line = functions.read_file_line(f).split('\t')
    prev_movie = {'name': None, 'year_id': None}
    prev_genre = None
    while line[0] != '':
        movie = functions.get_movie_split(line[0])
        genre = line[-1].replace('\n', '')
        if i % 1000 == 0:
            print(movie, i)
        if movie['name'] != prev_movie['name'] or movie['year_id'] != prev_movie['year_id'] or movie['year'] != \
                prev_movie['year'] or genre != prev_genre:
            insert_genre_to_movie(genre, movie)
            conn.commit()
            i += 1
            prev_movie = movie
            prev_genre = genre
        line = functions.read_file_line(f).split('\t')


# Add Genres
functions.jump_to_line_with_string(f, '8: THE GENRES LIST')
functions.jump_lines(f, 2)

conn = psycopg2.connect(variables.postgres_credentials)
cur = conn.cursor()

functions.reset_table(cur, 'genre_to_movie')

cur.execute("SET transform_null_equals TO ON")

functions.start_timer('Add genres to movies')
add_genres_to_movies()
functions.check_timer('Add genres to movies')

conn.commit()

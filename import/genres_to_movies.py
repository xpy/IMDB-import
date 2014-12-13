import psycopg2
import variables
import functions

fileName = 'genres.list'
f = open(variables.imdbFilesPath + fileName, 'r')


def insertGenreToMovie(genre, movie):
    # print( genre, movie)
    cur.execute("INSERT INTO genre_to_movie (genre_id,movie_id) "
                "SELECT genre.id,movie.id from genre,movie "
                "where genre.name = %s and movie.name = %s and movie.year_id = %s  "
                "AND NOT EXISTS ( SELECT 1 FROM genre_to_movie where genre_id = genre.id and movie_id = movie.id)",
                [genre, movie['name'], movie['year_id']])


def addGenresToMovies():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8').split('\t')
    movie = functions.getMovieSplit(line[0])
    genre = line[-1].replace('\n', '')
    prevMovie = {'name': None, 'year_id': None}
    prevGenre = None
    while line[0] != '':
        if i % 1000 == 0:
            print(movie, i)

        movie = functions.getMovieSplit(line[0])
        genre = line[-1].replace('\n', '')
        if (movie['name'] <> prevMovie['name'] and movie['year_id'] <> prevMovie['year_id'] and genre <> prevGenre ):
            insertGenreToMovie(genre, movie)
            i += 1
            prevMovie = movie
            prevGenre = genre
        line = f.readline().decode('iso-8859-1').encode('utf8').split('\t')


# Add Genres
functions.jumpToLineWithString(f, '8: THE GENRES LIST')
functions.jumpLines(f, 2)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

functions.startTimer('Add genres to movies')
addGenresToMovies()
functions.checkTimer('Add genres to movies')

conn.commit()

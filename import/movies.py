import psycopg2
import variables
import functions
import codecs

fileName = 'movies.list'
f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
fileEnd = '-----------------------------------------------------------------------------'


def insert_movie(movie):
    cur.execute(
        "INSERT INTO tmp_movie (name,year,year_id) SELECT %s,%s,%s ",
        [movie['name'], movie['year'], movie['year_id']])


def add_movies():
    i = 0
    line = functions.read_file_line(f)
    prev_movie = {'name': None, 'year': None, 'year_id': None}
    while line:
        movie = functions.get_movie_split(line)
        if movie is not None:
            i += 1
            if i % 10000 == 0:
                print(movie['name'] + ' - ' + str(i))
        if prev_movie['name'] != movie['name'] or prev_movie['year'] != movie['year'] or prev_movie['year_id'] != movie[
                'year_id']:
            insert_movie(movie)
            prev_movie = movie
        line = functions.read_file_line(f)
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = functions.read_file_line(f)
        if line.find(fileEnd) >= 0:
            return


functions.jump_to_line_with_string(f, '===========')
functions.jump_lines(f, 1)

functions.jump_lines(f, 0)

conn = psycopg2.connect(variables.postgres_credentials)
cur = conn.cursor()

functions.reset_table(cur, 'movie')
cur.execute("CREATE TEMP TABLE tmp_movie( name text, year integer, year_id integer );")

functions.start_timer('Add to tmp_table')
add_movies()
functions.check_timer('Add to tmp_table')

functions.start_timer('Insert to real table')
cur.execute("INSERT INTO movie (name,year,year_id) (SELECT DISTINCT name,year,year_id FROM tmp_movie ORDER BY name)")
functions.check_timer('Insert to real table')

functions.start_timer('Commit to DB')
conn.commit()
functions.check_timer('Commit to DB')

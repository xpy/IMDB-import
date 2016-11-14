import psycopg2
import variables
import functions
import codecs

fileName = 'genres.list'
f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')


def insert_genre(genre):
    print(genre)
    cur.execute(
        "INSERT INTO tmp_genre (name) SELECT %s ",
        [genre])


def add_genres():
    line = functions.read_file_line(f).split(' ')
    while line[0] != '\n':
        insert_genre(line[0])
        line = functions.read_file_line(f).split(' ')


# Add Genres
functions.jump_to_line_with_string(f, 'Breakdown of the main genres and the number of times they appear :')
functions.jump_lines(f, 1)

conn = psycopg2.connect(variables.postgres_credentials)
cur = conn.cursor()

functions.reset_table(cur, 'genre')

cur.execute("CREATE TEMP TABLE tmp_genre( name text );")

functions.start_timer('Add genres to tmp_table')
add_genres()
functions.check_timer('Add genres to tmp_table')

functions.start_timer('Add genres to real table')
cur.execute('INSERT INTO genre (name) (SELECT name FROM tmp_genre)')
functions.check_timer('Add genres to real table')

conn.commit()

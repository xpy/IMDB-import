import psycopg2
import variables
import functions

fileName = 'genres.list'
f = open(variables.imdbFilesPath + fileName, 'r')

def insertGenre(genre):
    print(genre)
    cur.execute(
        "INSERT INTO tmp_genre (name) SELECT %s ",
        [genre])

def addGenres():
    line = f.readline().decode('iso-8859-1').encode('utf8').split(' ')
    while line[0] != '\n':
        insertGenre(line[0])
        line = f.readline().decode('iso-8859-1').encode('utf8').split(' ')


# Add Genres
functions.jumpToLineWithString(f,'Breakdown of the main genres and the number of times they appear :')
functions.jumpLines(f,1)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

cur.execute("CREATE TEMP TABLE tmp_genre( name text );")

functions.startTimer('Add genres to tmp_table')
addGenres()
functions.checkTimer('Add genres to tmp_table')

functions.startTimer('Add genres to real table')
cur.execute('INSERT INTO genre (name) (SELECT name FROM tmp_genre)')
functions.checkTimer('Add genres to real table')

conn.commit()

import psycopg2
import variables
import functions

fileName = 'movies.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'

def insertMovie(movie):
    cur.execute(
        "INSERT INTO tmp_movie (name,year,year_id) SELECT %s,%s,%s ",
        [movie['name'], movie['year'], movie['year_id']])



def addMovies():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8')
    while line:
        movie = functions.getMovieSplit(line)
        if (movie != None):
            i += 1
            if i % 10000 == 0:
                print movie['name'] + ' - ' + str(i)
        insertMovie(movie)
        line = f.readline().decode('iso-8859-1').encode('utf8')
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline().decode('iso-8859-1').encode('utf8')
        if line.find(fileEnd) >= 0: return

functions.jumpToLineWithString(f,'===========')
functions.jumpLines(f,1)

functions.jumpLines(f,0)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()
cur.execute("CREATE TEMP TABLE tmp_movie(   name text,  year integer,  year_id text);")
functions.startTimer('Add to tmp_table')
addMovies()
functions.checkTimer('Add to tmp_table')
functions.startTimer('Insert to real table')
cur.execute("INSERT INTO movie (name,year,year_id) (SELECT DISTINCT name,year,year_id FROM tmp_movie ORDER BY NAME)")
functions.checkTimer('Insert to real table')
functions.startTimer('Commit to DB')
conn.commit()
functions.checkTimer('Commit to DB')



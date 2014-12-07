import re
import psycopg2
import variables
import functions

fileName = 'movies.list'
f = open(variables.imdbFilesPath + fileName, 'r')
movieRegEx = '\"*([^(")]*[^("|\s)])("|\s)*\(([^\)]*)'
fileEnd = '-----------------------------------------------------------------------------'

def getMovie(str):
    str = str.decode('iso-8859-1').encode('utf8')
    res = re.match(movieRegEx, str)
    if res == None:
        return None
    ret = {'name': res.groups()[0], 'year_id': res.groups()[2], 'year': None}

    # print res.groups()
    # print str
    # print ret

    if ret['year_id'] != None:
        ret['year'] = ret['year_id'].split('/')[0]
        if (ret['year'] == None or not ret['year'].isdigit()):
            ret['year'] = None
    return ret


def addMovies():
    i = 0
    line = f.readline()
    while line:
        movie = getMovie(line)
        if (movie != None):
            i += 1
            if i % 10000 == 0:
                print movie['name'] + ' ' + str(i)
                conn.commit()
            cur.execute(
                "INSERT INTO movie (name,year,year_id) SELECT %s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM movie WHERE name = %s)",
                [movie['name'], movie['year'], movie['year_id'], movie['name']])
        line = f.readline()
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline()
        if line.find(fileEnd) >= 0: return


functions.jumpToLineWithString(f,'===========')
functions.jumpLines(f,1)

functions.jumpLines(f,0)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

addMovies()

conn.commit()

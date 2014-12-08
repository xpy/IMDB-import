import re
import psycopg2
import variables
import functions

fileName = 'actors.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'

def insertActor(actor):
    cur.execute("INSERT INTO tmp_actor (name) SELECT %s",[actor])

def addActors():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8')
    while line:
        if line.find(fileEnd) >= 0: return
        splitLine = line.decode('iso-8859-1').encode('utf8').split('\t')
        actor = splitLine[0]
        i += 1
        if i % 10000 == 0:
            print actor + ' ' + str(i)
        insertActor(actor)
        line = f.readline()
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline()


functions.jumpToLineWithString(f, 'THE ACTORS LIST')
functions.jumpLines(f, 4)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

cur.execute("CREATE TEMP TABLE tmp_actor(name text);")

functions.startTimer('Add to tmp_table')
addActors()
functions.checkTimer('Add to tmp_table')

functions.startTimer('Insert to real table')
cur.execute("INSERT INTO actor (name) (SELECT DISTINCT name FROM tmp_actor ORDER BY name)")
functions.checkTimer('Insert to real table')

functions.startTimer('Commit to DB')
conn.commit()
functions.checkTimer('Commit to DB')

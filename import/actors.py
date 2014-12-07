import re
import psycopg2
import  variables
import functions

fileName = 'actors.list'
f = open(variables.imdbFilesPath + fileName, 'r')
actors = []

def getMovie(str):
    res = re.match('([^\(]*)\s\(([0-9]*)',str)
    return {'name':res.group(0),'year':res.group(1)}

def parse():
    line = f.readline()
    splitLine =  line.split('\t')
    actor = {}
    actor['name'] = splitLine[0]
    actor['movies'] = []
    actor['movies'].append( getMovie(splitLine[len(splitLine)-1]))
    line = f.readline()
    while len(line) != 1:
        splitLine =  line.split('\t')
        actor['movies'].append( getMovie(splitLine[len(splitLine)-1]))
        line = f.readline()
    actors.append(actor)

def addActors():
    i = 0
    line = f.readline()
    while line:
        splitLine =  line.split('\t')
        actor = splitLine[0].decode('iso-8859-1').encode('utf8')
        i+=1
        if i%10000 == 0:
            print actor +' '+ str(i)
            conn.commit()

        cur.execute("INSERT INTO actor (name) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM actor WHERE name = %s)", [actor,actor])
        line = f.readline()
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline()
        if line.find('-----------------------------------------------------------------------------') >=0: return

functions.jumpToLineWithString(f,'THE ACTORS LIST')
functions.jumpLines(f,4)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

addActors()
conn.commit()

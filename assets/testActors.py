import re
import psycopg2
import variables
import functions
import pickle

fileName = 'actresses.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'

def testActors():
    i = 0
    line = functions.readFileLine(f)
    dbActors = []
    conn = psycopg2.connect(variables.postgresCredentials)
    cur = conn.cursor()
    cur.execute("SELECT lname.name::text || ', ' || fname.name::text FROM actor,actor_name fname,actor_name lname WHERE fname.id = actor.fname_id and lname.id = actor.lname_id order by 1")
    for row in cur.fetchall():
        if(row[0] == 'Carell, Steve'):
            print('---------')
        if actors.count(row[0]) > 0:
            actors.remove(row[0])
        if actors.count(row[0]) > 0:
            actors.remove(row[0])

functions.jumpToLineWithString(f, 'THE ACTRESSES LIST')
functions.jumpLines(f, 4)

actors = pickle.load(open('../assets/top1000Actors_serialized.txt', 'r'))
testActors()
print(actors)
print(len(actors))
pickle.dump(actors,open('../assets/top1000Actors_serialized_rest2.txt','w'))
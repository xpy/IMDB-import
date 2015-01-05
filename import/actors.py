import re
import psycopg2
import variables
import functions
import pickle
import codecs
fileName = 'actors.list'
f = codecs.open(variables.imdbFilesPath + fileName, 'r','ISO 8859-1')
fileEnd = '-----------------------------------------------------------------------------'


def insertName(name):
    cur.execute("INSERT INTO actor_name (name) SELECT %s  WHERE NOT EXISTS (select 1 FROM actor_name WHERE name = %s )",
                [name, name])


def insertActor(actor):
    insertName(actor['fname'])
    insertName(actor['lname'])
    cur.execute("INSERT INTO tmp_actor (fname_id,lname_id,name_index,gender) SELECT fname.id,lname.id,%s,'m'"
                " FROM actor_name fname, actor_name lname where fname.name = %s and lname.name = %s",
                [actor['name_id'], actor['fname'], actor['lname']])


def addActors():
    i = 0
    line = functions.readFileLine(f)
    while line:
        if line.find(fileEnd) >= 0: return
        splitLine = line.split('\t')
        actorName = splitLine[0]
        actorNameOnly = re.sub('\s\([a-zA-Z]*\)$', '', actorName)
        if(actorNameOnly.find('Ferrer, Jos')==0):
            print(actorNameOnly)
            print(actors)
            print(actorName)
        isTop1000 = actors.count(actorNameOnly) > 0
        if isTop1000:
            actors.remove(actorNameOnly)
            print(actorName)
            i += 1
            if i % 10 == 0:
                print actorName + ' ' + str(i)
                conn.commit()
                functions.checkTimer('Add to tmp_table')
                # return
            actor = functions.getActor(actorName)
            insertActor(actor)
        line = f.readline()
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline()


functions.jumpToLineWithString(f, 'THE ACTORS LIST')
functions.jumpLines(f, 4)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

''' Insert top 1000 Actors into a List '''
actors = [ a.decode('utf-8') for a in pickle.load(codecs.open('../assets/top1000Actors_serialized.txt', 'r'))]

functions.resetTable(cur, 'actor')
functions.resetTable(cur, 'actor_name')

cur.execute("SET transform_null_equals TO ON")

cur.execute("CREATE TEMP TABLE tmp_actor(fname_id int,lname_id int,name_index smallint,gender char);")

functions.startTimer('Add to tmp_table')
addActors()
functions.checkTimer('Add to tmp_table')

functions.startTimer('Insert to real table')
cur.execute(
    "INSERT INTO actor (fname_id,lname_id,name_index,gender) "
    "(SELECT DISTINCT fname_id,lname_id,name_index,gender FROM tmp_actor ORDER BY fname_id)")
functions.checkTimer('Insert to real table')

functions.startTimer('Commit to DB')
conn.commit()
functions.checkTimer('Commit to DB')

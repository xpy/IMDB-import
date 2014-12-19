import re
import psycopg2
import variables
import functions

fileName = 'actresses.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'

def insertName(name):
    cur.execute("INSERT INTO actor_name (name) SELECT %s  WHERE NOT EXISTS (select 1 FROM actor_name WHERE name = %s )",[name,name])

def insertActor(actor):
    actor = functions.getActor(actor)
    insertName(actor['fname'])
    insertName(actor['lname'])
    cur.execute("INSERT INTO tmp_actor (fname_id,lname_id,name_index,gender) SELECT fname.id,lname.id,%s,'f'"
                " FROM actor_name fname, actor_name lname where fname.name = %s and lname.name = %s",[actor['name_id'],actor['fname'],actor['lname']])


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
            conn.commit()
            functions.checkTimer('Add to tmp_table')
            # return
        insertActor(actor)
        line = f.readline()
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline()


functions.jumpToLineWithString(f, 'THE ACTRESSES LIST')
functions.jumpLines(f, 4)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

# functions.resetTable(cur,'actor')
# functions.resetTable(cur,'actor_name')

cur.execute("DROP TABLE tmp_actor;")
cur.execute("CREATE UNLOGGED TABLE tmp_actor(fname_id int,lname_id int,name_index smallint,gender char);")

functions.startTimer('Add to tmp_table')
addActors()
functions.checkTimer('Add to tmp_table')

functions.startTimer('Insert to real table')
cur.execute(
    "INSERT INTO actor (fname_id,lname_id,name_index,gender) (SELECT DISTINCT fname_id,lname_id,name_index,gender FROM tmp_actor ORDER BY fname_id)")
functions.checkTimer('Insert to real table')

functions.startTimer('Commit to DB')
conn.commit()
functions.checkTimer('Commit to DB')

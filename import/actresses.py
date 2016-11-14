import re
import psycopg2
import variables
import functions
import pickle
import codecs

fileName = 'actresses.list'
f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
fileEnd = '-----------------------------------------------------------------------------'


def insert_name(name):
    cur.execute("INSERT INTO actor_name (name) SELECT %s  WHERE NOT EXISTS (select 1 FROM actor_name WHERE name = %s )",
                [name, name])


def insert_actor(actor):
    insert_name(actor['fname'])
    insert_name(actor['lname'])
    cur.execute("INSERT INTO tmp_actor (fname_id,lname_id,name_index,gender) SELECT fname.id,lname.id,%s,'f'"
                " FROM actor_name fname, actor_name lname where fname.name = %s and lname.name = %s",
                [actor['name_id'], actor['fname'], actor['lname']])


def add_actors():
    i = 0
    line = functions.read_file_line(f)
    while line:
        if line.find(fileEnd) >= 0:
            return
        actor_name = line.split('\t')[0]
        actor_name_only = re.sub('\s\([a-zA-Z]*\)$', '', actor_name)
        is_top1000 = actors.count(actor_name_only) > 0
        if is_top1000:
            actors.remove(actor_name_only)
            print(actor_name)
            i += 1
            if i % 10 == 0:
                print('----------' + str(i))
                conn.commit()
                functions.check_timer('Add to tmp_table')
            actor = functions.get_actor(actor_name)
            insert_actor(actor)
        line = f.readline()
        while line != '' and (len(line) == 1 or line[0] == '\t'):
            line = f.readline()


functions.jump_to_line_with_string(f, 'THE ACTRESSES LIST')
functions.jump_lines(f, 4)

conn = psycopg2.connect(variables.postgres_credentials)
cur = conn.cursor()

''' Insert top 1000 Actors into a List '''
actors = [a.decode('utf-8') for a in pickle.load(codecs.open('../assets/top1000Actors_serialized.txt', 'r'))]

# functions.resetTable(cur,'actor')
# functions.resetTable(cur,'actor_name')

cur.execute("SET transform_null_equals TO ON")

cur.execute("CREATE TEMP TABLE tmp_actor(fname_id int,lname_id int,name_index smallint,gender char);")

functions.start_timer('Add to tmp_table')
add_actors()
functions.check_timer('Add to tmp_table')

functions.start_timer('Insert to real table')
cur.execute(
    "INSERT INTO actor (fname_id,lname_id,name_index,gender) "
    "(SELECT DISTINCT fname_id,lname_id,name_index,gender FROM tmp_actor ORDER BY fname_id)")
functions.check_timer('Insert to real table')

functions.start_timer('Commit to DB')
conn.commit()
functions.check_timer('Commit to DB')

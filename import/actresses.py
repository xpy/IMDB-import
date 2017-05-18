import re
import psycopg2
import sys
import variables
import functions
import pickle
import codecs


class ActressesImport:
    fileName = 'actresses.list'
    f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
    fileEnd = '-----------------------------------------------------------------------------'
    cur = None
    conn = None
    actors = None

    @classmethod
    def insert_name(cls, name):
        cls.cur.execute(
            "INSERT INTO actor_name (name) SELECT %s  WHERE NOT EXISTS (select 1 FROM actor_name WHERE name = %s )",
            [name, name])

    @classmethod
    def insert_actor(cls, actor):
        cls.insert_name(actor['fname'])
        cls.insert_name(actor['lname'])
        cls.cur.execute("INSERT INTO tmp_actor (fname_id,lname_id,name_index,gender) SELECT fname.id,lname.id,%s,'f'"
                        " FROM actor_name fname, actor_name lname where fname.name = %s and lname.name = %s",
                        [actor['name_id'], actor['fname'], actor['lname']])

    @classmethod
    def add_actors(cls):
        i = 0
        line = functions.read_file_line(cls.f)
        while line:
            if line.find(cls.fileEnd) >= 0:
                return
            actor_name = line.split('\t')[0]
            actor_name_only = re.sub('\s\([a-zA-Z]*\)$', '', actor_name)
            is_top1000 = cls.actors.count(actor_name_only) > 0
            if is_top1000:
                cls.actors.remove(actor_name_only)
                print(actor_name)
                i += 1
                if i % 10 == 0:
                    print('----------' + str(i))
                    cls.conn.commit()
                    functions.check_timer('Add to tmp_table')
                actor = functions.get_actor(actor_name)
                try:
                    cls.insert_actor(actor)
                except:
                    print(sys.exc_info()[0])
                    print("FERROR ", [actor_name, actor])
            line = cls.f.readline()
            while line != '' and (len(line) == 1 or line[0] == '\t'):
                line = cls.f.readline()

    @classmethod
    def run(cls):
        functions.jump_to_line_with_string(cls.f, 'THE ACTRESSES LIST')
        functions.jump_lines(cls.f, 4)

        cls.conn = psycopg2.connect(variables.postgres_credentials)
        cls.cur = cls.conn.cursor()

        ''' Insert top 1000 Actors into a List '''
        cls.actors = pickle.load(codecs.open('../assets/top1000Actors_serialized.txt', 'rb'))
        print(cls.actors)
        # functions.resetTable(cur,'actor')
        # functions.resetTable(cur,'actor_name')

        cls.cur.execute("SET transform_null_equals TO ON")

        cls.cur.execute("CREATE TEMP TABLE tmp_actor(fname_id int,lname_id int,name_index smallint,gender char);")

        functions.start_timer('Add to tmp_table')
        cls.add_actors()
        functions.check_timer('Add to tmp_table')

        functions.start_timer('Insert to real table')
        cls.cur.execute(
            "INSERT INTO actor (fname_id,lname_id,name_index,gender) "
            "(SELECT DISTINCT fname_id,lname_id,name_index,gender FROM tmp_actor ORDER BY fname_id)")
        functions.check_timer('Insert to real table')

        functions.start_timer('Commit to DB')
        cls.conn.commit()
        functions.check_timer('Commit to DB')

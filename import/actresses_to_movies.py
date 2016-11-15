import re
import psycopg2
import variables
import functions
import pickle

fileName = 'actresses.list'
f = open(variables.imdb_files_path + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'


def add_role(role):
    cur.execute(
        "INSERT INTO role (name) SELECT %s WHERE NOT EXISTS ( SELECT 1 FROM role WHERE name = %s) ",
        [role, role])


def add_movie_to_actor_to_db(actor, movie):
    q = "INSERT INTO tmp_actor_to_movie (actor_id,movie_id,billing_position,role_id) " \
        " SELECT actor.id,movie.id,%s,role.id FROM actor" \
        " JOIN actor_name fname ON actor.fname_id = fname.id" \
        " JOIN actor_name lname ON lname.id = actor.lname_id" \
        " ,movie, role WHERE " \
        " fname.name = %s AND lname.name = %s AND actor.name_index = %s AND actor.gender = 'f' " \
        " AND movie.name = %s  AND movie.year_id = %s AND role.name = %s ;"
    cur.execute(q, [movie['billingPosition'], actor['fname'], actor['lname'], actor['name_id'], movie['name'],
                    movie['year_id'], movie['roles']])


def add_actors_to_movies():
    i = 0
    line = functions.read_file_line(f)
    functions.start_timer('Add Actor')
    k = 0
    while line:
        split_line = [a for a in line.split('\t') if a != '']
        actor_name = split_line[0]
        actor_name_only = re.sub('\s\([a-zA-Z]*\)$', '', actor_name)
        is_top1000 = actors.count(actor_name_only) > 0

        k += 1
        if k % 10000 == 0:
            print(k)

        if is_top1000:
            actors.remove(actor_name_only)
            actor = functions.get_actor(actor_name)
            print(actor)
            i += 1
            if i % 100 == 0:
                print(actor, str(i))
            functions.check_timer('Add Actor')

            functions.start_timer('Deleting Duplicates')
            cur.execute("DELETE FROM tmp_actor_to_movie WHERE id NOT IN "
                        "(SELECT min(id) FROM tmp_actor_to_movie GROUP BY actor_id,movie_id)")
            functions.check_timer('Deleting Duplicates')

            functions.start_timer('Insert to real table')
            cur.execute("INSERT INTO actor_to_movie(actor_id ,movie_id,billing_position,role_id) SELECT DISTINCT "
                        "actor_id,movie_id,billing_position,role_id FROM tmp_actor_to_movie;")
            functions.check_timer('Insert to real table')

            cur.execute("DELETE FROM tmp_actor_to_movie")
            functions.start_timer('Add Actor')
            functions.check_timer('Add all Actors')
            # return
            movie = functions.get_movie(split_line[1])
            add_role(movie['roles'])
            add_movie_to_actor_to_db(actor, movie)
            line = functions.read_file_line(f)
            while len(line) != 1:
                split_line = [a for a in line.split('\t') if a != '']
                movie_split = functions.get_movie_split(split_line[0])
                if movie_split['name'] != movie['name'] or movie_split['year_id'] != movie['year_id']:
                    movie = functions.get_movie(split_line[0])
                    add_role(movie['roles'])
                    add_movie_to_actor_to_db(actor, movie)
                line = functions.read_file_line(f)
            conn.commit()
            line = functions.read_file_line(f)
            if line.find(fileEnd) >= 0:
                return
        else:
            while len(line) != 1:
                line = functions.read_file_line(f)
            line = functions.read_file_line(f)
            if line.find(fileEnd) >= 0:
                return


functions.jump_to_line_with_string(f, 'THE ACTRESSES LIST')
functions.jump_lines(f, 4)
# 236
# functions.jumpLines(f,  2117917 -240 )

conn = psycopg2.connect(variables.postgres_credentials)
cur = conn.cursor()

''' Insert top 1000 Actors into a List '''
actors = pickle.load(open('../assets/top1000Actors_serialized.txt', 'rb'))
# functions.resetTable(cur, 'role')
# functions.resetTable(cur, 'actor_to_movie')

cur.execute("SET transform_null_equals TO ON")
cur.execute("CREATE TEMP TABLE tmp_actor_to_movie"
            "(id serial ,actor_id int,movie_id int,billing_position int,role_id integer);")

functions.start_timer('Add all Actors')
add_actors_to_movies()
functions.check_timer('Add all Actors')

"""
cur.execute("select * from tmp_actor_to_movie")
rows = cur.fetchall()
for row in rows:
    print "   ", row

"""

functions.start_timer('Commit to DB')
conn.commit()
functions.check_timer('Commit to DB')

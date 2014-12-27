import re
import psycopg2
import variables
import functions
import pickle

fileName = 'actors.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'


def addRole(role):
    cur.execute(
        "INSERT INTO role (name) SELECT %s WHERE NOT EXISTS ( SELECT 1 FROM role WHERE name = %s) ",
        [role, role])


def addMovieToActorToDB(actor, movie):
    q = "INSERT INTO tmp_actor_to_movie (actor_id,movie_id,billing_position,role_id) " \
        " SELECT actor.id,movie.id,%s,role.id FROM actor" \
        " JOIN actor_name fname ON actor.fname_id = fname.id" \
        " JOIN actor_name lname ON lname.id = actor.lname_id" \
        " ,movie, role WHERE " \
        " fname.name = %s AND lname.name = %s AND actor.name_index = %s AND actor.gender = 'm' " \
        " AND movie.name = %s  AND movie.year_id = %s AND role.name = %s ;"
    cur.execute(q, [movie['billingPosition'], actor['fname'], actor['lname'], actor['name_id'], movie['name'],
                    movie['year_id'], movie['roles']])


def addActorsToMovies():
    i = 0
    line = functions.readFileLine(f)
    functions.startTimer('Add Actor')
    k = 0
    while line:
        splitLine = [a for a in line.split('\t') if a != '']
        actorName = splitLine[0]
        isTop1000 = actors.count(actorName) > 0

        k += 1
        if k % 10000 == 0:
            print k

        if isTop1000:
            actors.remove(actorName)
            actor = functions.getActor(actorName)
            print(actor)
            i += 1
            if i % 100 == 0:
                print actor, str(i)
                functions.checkTimer('Add Actor')

                functions.startTimer('Deleting Duplicates')
                cur.execute("DELETE FROM tmp_actor_to_movie WHERE id NOT IN "
                            "(SELECT min(id) FROM tmp_actor_to_movie GROUP BY actor_id,movie_id)")
                functions.checkTimer('Deleting Duplicates')

                functions.startTimer('Insert to real table')
                cur.execute("INSERT INTO actor_to_movie(actor_id ,movie_id,billing_position,role_id) SELECT DISTINCT "
                            "actor_id,movie_id,billing_position,role_id FROM tmp_actor_to_movie;")
                functions.checkTimer('Insert to real table')

                cur.execute("DELETE FROM tmp_actor_to_movie")
                functions.startTimer('Add Actor')
                functions.checkTimer('Add all Actors')
                conn.commit()
                # return
            movie = functions.getMovie(splitLine[1])
            addRole(movie['roles'])
            addMovieToActorToDB(actor, movie)
            line = functions.readFileLine(f)
            while len(line) != 1:
                splitLine = [a for a in line.split('\t') if a != '']
                movieSplit = functions.getMovieSplit(splitLine[0])
                if movieSplit['name'] != movie['name'] or movieSplit['year_id'] != movie['year_id']:
                    movie = functions.getMovie(splitLine[0])
                    addRole(movie['roles'])
                    addMovieToActorToDB(actor, movie)
                line = functions.readFileLine(f)
            line = functions.readFileLine(f)
            if line.find(fileEnd) >= 0: return
        else:
            while len(line) != 1:
                line = functions.readFileLine(f)
            line = functions.readFileLine(f)
            if line.find(fileEnd) >= 0: return


functions.jumpToLineWithString(f, 'THE ACTORS LIST')
functions.jumpLines(f, 4)
# 236
# functions.jumpLines(f,  2117917 -240 )

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

''' Insert top 1000 Actors into a tmp table '''
actors = pickle.load(open('../assets/top1000Actors_serialized.txt', 'r'))
# functions.resetTable(cur, 'role')
functions.resetTable(cur, 'actor_to_movie')
cur.execute("SET transform_null_equals TO ON")
cur.execute("CREATE TEMP TABLE tmp_actor_to_movie"
            "(id serial ,actor_id int,movie_id int,billing_position int,role_id integer);")

functions.startTimer('Add all Actors')
addActorsToMovies()
functions.checkTimer('Add all Actors')

"""
cur.execute("select * from tmp_actor_to_movie")
rows = cur.fetchall()
for row in rows:
    print "   ", row

"""

functions.startTimer('Commit to DB')
conn.commit()
functions.checkTimer('Commit to DB')

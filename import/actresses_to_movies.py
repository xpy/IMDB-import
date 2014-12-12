import re
import psycopg2
import variables
import functions

fileName = 'actresses.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'
actors = []


def addMovieToActorToDB(actor, movie):
    # print(movie)
    # print "INSERT INTO actor_to_movie (actor_id,movie_id) SELECT actor.id,movie.id FROM actor,movie WHERE actor.name = %s AND movie.name = %s AND movie.year_id = %s" % (actor,movie['name'],movie['year_id'])
    # print(movie)
    cur.execute("INSERT INTO tmp_actor_to_movie (actor_id,movie_id,billing_position,roles) "
                "SELECT actor.id,movie.id,%s,%s FROM actor,movie WHERE actor.name = %s AND movie.name = %s and actor.gender = 'f' "
                "AND movie.year_id = %s "
                , [movie['billingPosition'], movie['roles'], actor, movie['name'], movie['year_id']])
    # "AND NOT EXISTS ( SELECT 1 FROM tmp_actor_to_movie WHERE actor_id = actor.id AND movie_id = movie.id)"


def addActorsToMovies():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8')
    functions.startTimer('Add Actor')

    while line:
        splitLine = [a for a in line.split('\t') if a != '']
        actor = splitLine[0]
        i += 1
        if i % 10000 == 0:
            print actor + ' ' + str(i)
            functions.checkTimer('Add Actor')
            functions.startTimer('Deleting Duplicates')
            cur.execute("DELETE FROM tmp_actor_to_movie WHERE id NOT IN "
                        "(SELECT min(id) FROM tmp_actor_to_movie GROUP BY actor_id,movie_id)")
            functions.checkTimer('Deleting Duplicates')
            functions.startTimer('Insert to real table')
            cur.execute("INSERT INTO actor_to_movie(actor_id ,movie_id,billing_position,roles) SELECT DISTINCT "
                        "actor_id,movie_id,billing_position,roles FROM tmp_actor_to_movie;")
            functions.checkTimer('Insert to real table')
            cur.execute("DELETE FROM tmp_actor_to_movie")
            functions.startTimer('Add Actor')
            functions.checkTimer('Add all Actors')
            conn.commit()

            # return
        movie = functions.getMovie(splitLine[1])
        addMovieToActorToDB(actor, movie)
        line = f.readline().decode('iso-8859-1').encode('utf8')
        while len(line) != 1:
            splitLine = [a for a in line.split('\t') if a != '']
            movieSplit = functions.getMovieSplit(splitLine[0])
            if movieSplit['name'] != movie['name']:
                movie = functions.getMovie(splitLine[0])
                addMovieToActorToDB(actor, movie)
            line = f.readline().decode('iso-8859-1').encode('utf8')
        line = f.readline().decode('iso-8859-1').encode('utf8')
        if line.find(fileEnd) >= 0: return


functions.jumpToLineWithString(f, 'THE ACTRESSES LIST')
functions.jumpLines(f, 4)
# 236
# functions.jumpLines(f,  2117917 -240 )

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

cur.execute(
    "CREATE TEMP TABLE tmp_actor_to_movie(id serial ,actor_id int,movie_id int,billing_position int,roles text);")

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

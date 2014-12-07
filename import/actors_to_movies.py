import re
import psycopg2
import variables
import functions

fileName = 'actors.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '-----------------------------------------------------------------------------'
actors = []

def addMovieToActorToDB(actor,movie):
    # print(movie)
    # print "INSERT INTO actor_to_movie (actor_id,movie_id) SELECT actor.id,movie.id FROM actor,movie WHERE actor.name = %s AND movie.name = %s AND movie.year_id = %s" % (actor,movie['name'],movie['year_id'])
    cur.execute("INSERT INTO actor_to_movie (actor_id,movie_id) SELECT actor.id,movie.id FROM actor,movie WHERE actor.name = %s AND movie.name = %s AND movie.year_id = %s AND NOT EXISTS (SELECT 1 FROM actor_to_movie WHERE actor_id = actor.id AND movie_id = movie.id ) ",[actor,movie['name'],movie['year_id']])

def addActorsToMovies():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8')
    while line:
        splitLine = [a for a in line.split('\t') if a != '']
        actor = splitLine[0]
        i += 1
        if i % 100 == 0:
            print actor + ' ' + str(i)
            conn.commit()
        movie = functions.getMovieSplit(splitLine[1])
        addMovieToActorToDB(actor,movie)
        line = f.readline().decode('iso-8859-1').encode('utf8')
        while len(line) != 1:
            splitLine = [a for a in line.split('\t') if a != '']
            movie = functions.getMovieSplit(splitLine[0])
            addMovieToActorToDB(actor,movie)
            line = f.readline().decode('iso-8859-1').encode('utf8')
        line = f.readline().decode('iso-8859-1').encode('utf8')
        if line.find(fileEnd) >= 0: return


functions.jumpToLineWithString(f, 'THE ACTORS LIST')
functions.jumpLines(f, 4)
# 238
# functions.jumpLines(f,  32533 -238 )

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()

addActorsToMovies()
conn.commit()

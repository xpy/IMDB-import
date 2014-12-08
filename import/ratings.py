import re
import psycopg2
import variables
import functions

fileName = 'ratings.list'
f = open(variables.imdbFilesPath + fileName, 'r')
fileEnd = '--------------------------------------------------------------------'

def addRatings():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8')
    while line:
        rating = line.split()
        if(re.match('\{.*\}',rating[len(rating) -1]) < 0 ):
            finalRating = {'rating': rating[2], 'votes': rating[1]}
            rating = ' '.join(rating[3:])
            movie = functions.getMovieSplit(rating)
            i += 1
            if i % 10000 == 0:
                print rating + str(i)
            cur.execute("UPDATE movie SET rating = %s, votes = %s WHERE name = %s and year_id = %s",
                        [finalRating['rating'], finalRating['votes'], movie['name'], movie['year_id']])
        line = f.readline().decode('iso-8859-1').encode('utf8')
        while line != '' and line.find(fileEnd) < 0 and (
                len(line) == 1 or line[0] != ' '):
            line = f.readline().decode('iso-8859-1').encode('utf8')

        if line.find(fileEnd) >= 0: return


functions.jumpToLineWithString(f,'New  Distribution  Votes  Rank  Title')
functions.jumpLines(f,0)

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()
functions.startTimer('Add ratings')
addRatings()
functions.checkTimer('Add ratings')
functions.startTimer('Commit to DB')
conn.commit()
functions.checkTimer('Commit to DB')

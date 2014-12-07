import re
import psycopg2
import  variables

fileName = 'ratings.list'
f = open(variables.imdbFilesPath + fileName, 'r')


def getMovie(str):
    res = re.match('\"([^\"]*)\"+\s+\(([0-9]*)', str)
    ret = {'name': res.groups()[0].decode('iso-8859-1').encode('utf8'),
           'year': res.groups()[1].decode('iso-8859-1').encode('utf8')}
    if ret['year'] == '':
        ret['year'] = None
    return ret


def addRatings():
    i = 0
    line = f.readline().decode('iso-8859-1').encode('utf8')
    while line:
        rating = line.split()
        finalRating = {}
        finalRating['rating'] = rating[2]
        finalRating['votes'] = rating[1]
        movieName = []
        k = 3
        # print(rating)
        while k < len(rating)-1 and re.match('\(.*\)', rating[k]) == None:
            movieName.append(rating[k])
            k += 1
        finalRating['movieName'] = ' '.join(movieName).replace('"', '')
        finalRating['year_id'] = rating[k].replace('(', '').replace(')', '')
        print(finalRating)

        # print( [rating[2], rating[1], ' '.join(rating[3:len(rating) - 2]), rating[len(rating) - 1]])
        i += 1
        if i % 10000 == 0:
            print(rating)
            print(finalRating)
            conn.commit()
        cur.execute("UPDATE movie SET rating = %s, votes = %s WHERE name = %s and year_id = %s",
                    [finalRating['rating'], finalRating['votes'], finalRating['movieName'], finalRating['year_id']])
        line = f.readline().decode('iso-8859-1').encode('utf8')
        while line != '' and line.find('--------------------------------------------------------------------') < 0 and (len(line) == 1 or line[0] != ' '):
            line = f.readline().decode('iso-8859-1').encode('utf8')

        if line.find('--------------------------------------------------------------------') >= 0: return


line = f.readline()
while line.find('New  Distribution  Votes  Rank  Title') < 0:
    line = f.readline()
for i in range(0,570000) :
    line = f.readline()

conn = psycopg2.connect(variables.postgresCredentials)
cur = conn.cursor()
addRatings()
conn.commit()

import re
import psycopg2
import variables
import functions

fileName = 'ratings.list'
f = open(variables.imdb_files_path + fileName, 'r')
fileEnd = '--------------------------------------------------------------------'


def add_ratings():
    i = 0
    line = f.readline()
    while line:
        if re.match('.*\{.*\}$', line) is None:
            rating = line.split()
            final_rating = {'rating': rating[2], 'votes': rating[1]}
            rating = ' '.join(rating[3:])
            movie = functions.get_movie_split(rating)
            i += 1
            if i % 10000 == 0:
                print(rating + ' ' + str(i))
            cur.execute("UPDATE movie SET rating = %s, votes = %s WHERE name = %s and year = %s and year_id = %s",
                        [final_rating['rating'], final_rating['votes'], movie['name'], movie['year'], movie['year_id']])
        line = f.readline()
        while line != '' and line.find(fileEnd) < 0 and (
                        len(line) == 1 or line[0] != ' '):
            line = f.readline()

        if line.find(fileEnd) >= 0:
            return


functions.jump_to_line_with_string(f, 'New  Distribution  Votes  Rank  Title')
functions.jump_lines(f, 0)

conn = psycopg2.connect(variables.postgres_credentials)
cur = conn.cursor()
cur.execute("SET transform_null_equals TO ON")

functions.start_timer('Add ratings')
add_ratings()
functions.check_timer('Add ratings')
functions.start_timer('Commit to DB')
conn.commit()
functions.check_timer('Commit to DB')

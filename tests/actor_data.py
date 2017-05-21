import psycopg2

import variables


def print_results(cur):
    rows = cur.fetchall()
    for row in rows:
        print("   ", row)


actor_id = 3
conn = psycopg2.connect(variables.postgres_credentials_new)
cur = conn.cursor()
cur.execute("SET search_path TO light;")
cur.execute('SELECT fname.name,lname.name from light.actor actor '
            'JOIN actor_name fname ON fname_id = fname.id '
            'JOIN actor_name lname on lname_id = lname.id '
            'WHERE actor.id = %s ' % actor_id)
print('-----ACTOR-----')
print_results(cur)
cur.execute('SELECT * from light."CF_get_actor_genre_rating"(%s)' % actor_id)
print('-----RATINGS-----')
print_results(cur)
print('-----MOVIES-----')
cur.execute('SELECT * FROM light."CF_get_actor_movies"(%s)' % actor_id)
print_results(cur)

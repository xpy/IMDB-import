import re
import psycopg2
import variables
import functions
import pickle
import codecs


class ActorsToMoviesImport:
    fileName = 'actors.list'
    f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
    fileEnd = '-----------------------------------------------------------------------------'
    cur = None
    conn = None

    @classmethod
    def add_role(cls, role):
        cls.cur.execute(
            "INSERT INTO role (name) SELECT %s WHERE NOT EXISTS ( SELECT 1 FROM role WHERE name = %s) ",
            [role, role])

    @classmethod
    def add_movie_to_actor_to_db(cls, actor, movie):
        q = "INSERT INTO tmp_actor_to_movie (actor_id,movie_id,billing_position,role_id) " \
            " SELECT actor.id,movie.id,%s,role.id FROM actor" \
            " JOIN actor_name fname ON actor.fname_id = fname.id" \
            " JOIN actor_name lname ON lname.id = actor.lname_id" \
            " ,movie, role WHERE " \
            " fname.name = %s AND lname.name = %s AND actor.name_index = %s AND actor.gender = 'm' " \
            " AND movie.name = %s  AND movie.year = %s AND movie.year_id = %s AND role.name = %s ;"
        cls.cur.execute(q, [movie['billingPosition'], actor['fname'], actor['lname'], actor['name_id'], movie['name'],
                            movie['year'], movie['year_id'], movie['roles']])

    @classmethod
    def delete_duplicates(cls):
        cls.cur.execute("DELETE FROM tmp_actor_to_movie WHERE id NOT IN "
                        "(SELECT min(id) FROM tmp_actor_to_movie GROUP BY actor_id,movie_id)")

    @classmethod
    def insert_into_real_table(cls):
        cls.cur.execute("INSERT INTO actor_to_movie(actor_id ,movie_id,billing_position,role_id) SELECT DISTINCT "
                        "actor_id,movie_id,billing_position,role_id FROM tmp_actor_to_movie;")

    @classmethod
    def add_actors_to_movies(cls):
        i = 0
        line = functions.read_file_line(cls.f)
        functions.start_timer('Add Actor')
        k = 0
        while line:
            split_line = [a for a in line.split('\t') if a != '']
            actor_name = split_line[0]
            actor_name_only = re.sub('\s\([a-zA-Z]*\)$', '', actor_name)
            is_top1000 = cls.actors.count(actor_name_only) > 0

            k += 1
            if k % 10000 == 0:
                print(k)

            if is_top1000:
                cls.actors.remove(actor_name_only)
                actor = functions.get_actor(actor_name)
                print(actor)
                i += 1
                if i % 100 == 0:
                    print('------------' + str(i))
                functions.check_timer('Add Actor')

                functions.start_timer('Deleting Duplicates')
                cls.delete_duplicates()
                functions.check_timer('Deleting Duplicates')

                functions.start_timer('Insert to real table')
                cls.insert_into_real_table()
                functions.check_timer('Insert to real table')

                cls.cur.execute("DELETE FROM tmp_actor_to_movie")

                functions.start_timer('Add Actor')
                functions.check_timer('Add all Actors')

                movie = functions.get_movie(split_line[1])
                if movie:
                    cls.add_role(movie['roles'])
                    cls.add_movie_to_actor_to_db(actor, movie)

                line = functions.read_file_line(cls.f)
                while len(line) != 1:
                    split_line = [a for a in line.split('\t') if a != '']
                    movie_split = functions.get_movie_split(split_line[0])
                    if movie_split and movie and (
                            movie_split['name'] != movie['name'] or movie_split['year_id'] != movie['year_id']):
                        movie = functions.get_movie(split_line[0])
                        if movie:
                            cls.add_role(movie['roles'])
                            cls.add_movie_to_actor_to_db(actor, movie)
                    line = functions.read_file_line(cls.f)
                cls.conn.commit()
                line = functions.read_file_line(cls.f)
                if line.find(cls.fileEnd) >= 0:
                    return
            else:
                while len(line) != 1:
                    line = functions.read_file_line(cls.f)
                line = functions.read_file_line(cls.f)
                if line.find(cls.fileEnd) >= 0:
                    return

    @classmethod
    def run(cls, conn):
        functions.jump_to_line_with_string(cls.f, 'THE ACTORS LIST')
        functions.jump_lines(cls.f, 4)
        # 236
        # functions.jumpLines(f,  2117917 -240 )

        cls.conn = conn
        cls.cur = cls.conn.cursor()

        ''' Insert top 1000 Actors into a List '''
        cls.actors = pickle.load(codecs.open('./assets/top1000Actors_serialized.txt', 'rb'))
        # functions.resetTable(cls.cur, 'role')
        functions.reset_table(cls.cur, 'actor_to_movie')

        cls.cur.execute("SET transform_null_equals TO ON")
        cls.cur.execute("CREATE TEMP TABLE tmp_actor_to_movie"
                        "(id serial ,actor_id int,movie_id int,billing_position int,role_id integer);")

        functions.start_timer('Add all Actors')
        cls.add_actors_to_movies()
        functions.check_timer('Add all Actors')

        cls.cur.execute("DROP TABLE tmp_actor_to_movie CASCADE")

        """
        cls.cur.execute("select * from tmp_actor_to_movie")
        rows = cls.cur.fetchall()
        for row in rows:
            print "   ", row
        
        """

        functions.start_timer('Commit to DB')
        cls.conn.commit()
        functions.check_timer('Commit to DB')

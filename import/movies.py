import psycopg2
import variables
import functions
import codecs


class MoviesImport:
    fileName = 'movies.list'
    f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
    fileEnd = '-----------------------------------------------------------------------------'
    cur = None
    conn = None

    @classmethod
    def insert_movie(cls, movie):
        # if movie['year_id'] is not None:
        #     print([movie['name'], movie['year'], movie['year_id']])
        cls.cur.execute(
            "INSERT INTO tmp_movie (name,year,year_id) SELECT %s,%s,%s ",
            [movie['name'], movie['year'], movie['year_id']])

    @classmethod
    def add_movies(cls):
        i = 0
        line = functions.read_file_line(cls.f)
        prev_movie = {'name': None, 'year': None, 'year_id': None}
        while line:
            movie = functions.get_movie_split(line)
            if movie is not None:
                i += 1
                if i % 10000 == 0:
                    print(movie['name'] + ' - ' + str(i))
            if prev_movie['name'] != movie['name'] or prev_movie['year'] != movie['year'] or prev_movie['year_id'] != \
                    movie[
                        'year_id']:
                cls.insert_movie(movie)
                prev_movie = movie
            line = functions.read_file_line(cls.f)
            while line != '' and (len(line) == 1 or line[0] == '\t'):
                line = functions.read_file_line(cls.f)
            if line.find(cls.fileEnd) >= 0:
                return

    @classmethod
    def run(cls, conn):
        functions.jump_to_line_with_string(cls.f, '===========')
        functions.jump_lines(cls.f, 1)

        functions.jump_lines(cls.f, 0)

        cls.conn = conn
        cls.cur = cls.conn.cursor()

        functions.reset_table(cls.cur, 'movie')
        cls.cur.execute("CREATE TEMP TABLE tmp_movie( name text, year integer, year_id integer );")

        functions.start_timer('Add to tmp_table')
        cls.add_movies()
        functions.check_timer('Add to tmp_table')

        functions.start_timer('Insert to real table')
        cls.cur.execute(
            "INSERT INTO movie (name,year,year_id) (SELECT DISTINCT name,year,year_id FROM tmp_movie ORDER BY name)")
        functions.check_timer('Insert to real table')

        functions.start_timer('Commit to DB')
        cls.conn.commit()
        functions.check_timer('Commit to DB')

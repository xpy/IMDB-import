import psycopg2
import variables
import functions
import codecs


class GenresImport:
    fileName = 'genres.list'
    f = codecs.open(variables.imdb_files_path + fileName, 'r', 'ISO 8859-1')
    cur = None
    conn = None

    @classmethod
    def insert_genre(cls, genre):
        print(genre)
        cls.cur.execute(
            "INSERT INTO tmp_genre (name) SELECT %s ",
            [genre])

    @classmethod
    def add_genres(cls):
        line = functions.read_file_line(cls.f).split(' ')
        while line[0] != '\n':
            cls.insert_genre(line[0])
            line = functions.read_file_line(cls.f).split(' ')

    @classmethod
    def run(cls, conn):
        functions.jump_to_line_with_string(cls.f, 'Breakdown of the main genres and the number of times they appear :')
        functions.jump_lines(cls.f, 1)

        cls.conn = conn
        cls.cur = cls.conn.cursor()

        functions.reset_table(cls.cur, 'genre')

        cls.cur.execute("CREATE TEMP TABLE tmp_genre( name text );")

        functions.start_timer('Add genres to tmp_table')
        cls.add_genres()
        functions.check_timer('Add genres to tmp_table')

        functions.start_timer('Add genres to real table')
        cls.cur.execute('INSERT INTO genre (name) (SELECT name FROM tmp_genre)')
        functions.check_timer('Add genres to real table')

        cls.conn.commit()

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from functions import *

directory = "schema/"


def create_schema(conn):
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Main tables
    executeScriptsFromFile(directory + "actor_name.schema.sql", cur)
    executeScriptsFromFile(directory + "actor.schema.sql", cur)
    executeScriptsFromFile(directory + "movie.schema.sql", cur)
    executeScriptsFromFile(directory + "genre.schema.sql", cur)
    executeScriptsFromFile(directory + "role.schema.sql", cur)

    # Relational Tables
    executeScriptsFromFile(directory + "actor_to_movie.schema.sql", cur)
    executeScriptsFromFile(directory + "genre_to_movie.schema.sql", cur)

    # Initialization
    executeScriptsFromFile(directory + "set_movie_genre.sql", cur)

    # Views
    executeScriptsFromFile(directory + "VW_movie.schema.sql", cur)

    # Functions
    executeScriptsFromFile(directory + "get_actor_genre_rating.function.sql", cur)
    executeScriptsFromFile(directory + "get_actor_movies.function.sql", cur)

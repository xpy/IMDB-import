import psycopg2

import variables
from actors import ActorImport
from actors_to_movies import ActorsToMoviesImport
from actresses import ActressesImport
from actresses_to_movies import ActressesToMoviesImport
from functions import runInParallel
from genres import GenresImport
from genres_to_movies import GenresToMoviesImport
from movies import MoviesImport
from ratings import RatingsImport
from schema.create_schema import create_schema

conn = psycopg2.connect(variables.postgres_credentials_new)

# create_schema(conn)
#
# ActorImport.run(conn)
# ActressesImport.run(conn)
# # runInParallel()
# GenresImport.run(conn)
# MoviesImport.run(conn)
ActorsToMoviesImport.run(conn)
ActressesToMoviesImport.run(conn)

GenresToMoviesImport.run(conn)
RatingsImport.run(conn)

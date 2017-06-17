import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from schema.create_schema import create_schema

from functions import executeScriptsFromFile
import variables

directory = "schema/"

conn = psycopg2.connect(variables.postgres_credentials)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
executeScriptsFromFile(directory + "create_light_schema.sql", cur)

cur.execute("SET search_path TO light;")
create_schema(conn)
executeScriptsFromFile(directory + "import_to_light.sql", cur)

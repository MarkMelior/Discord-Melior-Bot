import pymysql

# SERVER SQL
# import urllib.parse as up
# import psycopg2
# up.uses_netloc.append("postgres")
# connection = psycopg2.connect("dbname='umbzoezm' user='umbzoezm' host='mahmud.db.elephantsql.com' password='NP0ecKUoXz3wyoXO_cYCwMZcTZ2h1iT2'")



# LOCALHOST SQL
HOST = '127.0.0.1'
USER = 'root'
PASSWORD = ''
DB_NAME = 'discord'
PORT = 3306
connection = pymysql.connect(
    host = HOST,
    port = PORT,
    user = USER,
    password = PASSWORD,
    database = DB_NAME
)



cursor = connection.cursor()
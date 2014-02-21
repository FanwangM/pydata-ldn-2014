import psycopg2

import pandas as pd

cx = psycopg2.connect(user="pydata", password="pydata", dbname="emails", host="localhost")
df = pd.io.sql.read_sql("SELECT data->'From', data->'Date', data->'Subject' FROM pylist", cx)

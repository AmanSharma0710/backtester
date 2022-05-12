# from ninja_trader.constants.constants import *
import math
import datetime
import time
import threading
import psycopg2
from numpy import dtype
import sys
sys.path.append('../')
from constants import *

def create_connection():
    conn = psycopg2.connect(f"dbname={db_name} user={user_name} host={host_name} password={password} port={postgres_port}")
    return conn

def create_table(conn, table_name):
    cur = conn.cursor()
    # CREATE TABLE IF NOT EXISTS public.nifty_500
    # (
    #     date integer NOT NULL,
    #     "time" integer NOT NULL,
    #     open real,
    #     high real,
    #     low real,
    #     close real,
    #     volume integer,
    #     CONSTRAINT nifty_500_pkey PRIMARY KEY (date, "time")
    # )
    cur.execute(f'DROP TABLE IF EXISTS public."{table_name}";')
    cur.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (date integer NOT NULL, "time" integer NOT NULL, open real, high real, low real, close real, volume integer, oi integer, CONSTRAINT "{table_name}_pkey" PRIMARY KEY (date, "time"));')
    # CREATE INDEX IF NOT EXISTS data_index
    # ON public.nifty_500 USING btree
    # (date ASC NULLS LAST)
    # TABLESPACE pg_default;
    cur.execute(f'CREATE INDEX IF NOT EXISTS "{table_name}_data_index" ON "{table_name}" USING btree (date ASC NULLS LAST) TABLESPACE pg_default;')
    # CREATE INDEX IF NOT EXISTS time_index
    # ON public.nifty_500 USING btree
    # ("time" ASC NULLS LAST)
    # TABLESPACE pg_default;
    cur.execute(f'CREATE INDEX IF NOT EXISTS "{table_name}_time_index" ON "{table_name}" USING btree ("time" ASC NULLS LAST) TABLESPACE pg_default;')
    conn.commit()
    cur.close()

def describe_table(conn, table_name):
    cur = conn.cursor()
    query = f"SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    return res

def close_connection(conn):
    conn.close()

def insert_row(conn, table_name, date, time, open, high, low, close, volume, oi):
    cur = conn.cursor()
    cur.execute(f'INSERT INTO "{table_name}" (Date, Time, Open, High, Low, Close, Volume, Oi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
               (date, time, open, high, low, close, volume, oi))
    conn.commit()

def select_all_rows(conn):
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    res =  cur.fetchall()
    cur.close()
    return res

def fetch_all_table_names(conn):
    tables = []
    cur = conn.cursor()
    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    for table in cur.fetchall():
        tables.append(table[0])
    return set(tables)
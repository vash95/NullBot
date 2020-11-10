import psycopg2

import os
from configparser import ConfigParser
from collections import OrderedDict


def ini_to_dict(path):
    config = ConfigParser()
    config.read(path)
    return_value = OrderedDict()
    for section in reversed(config.sections()):
        return_value[section] = OrderedDict()
        section_tuples = config.items(section)
        for itemTurple in reversed(section_tuples):
            return_value[section][itemTurple[0]] = itemTurple[1]
    return return_value

settings = ini_to_dict(os.path.join(os.path.dirname(__file__), "config.ini"))

def query(query):
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = connect()
        conn.autocommit = True
        cur = conn.cursor()
        print(query)
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def select(query):
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = connect()
        conn.autocommit = True
        cur = conn.cursor()
        print(query)
        cur.execute(query)
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def connect():
    return psycopg2.connect(
            host=settings["postgresql"]["host"],
            database=settings["postgresql"]["database"],
            user=settings["postgresql"]["user"],
            password=settings["postgresql"]["password"])
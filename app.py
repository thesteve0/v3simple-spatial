__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, post, DEBUG
import os
import random
from random_words import RandomWords


@route('/')
def index():
    return "<h1> hello OpenShift Ninja without DB</h1>"


# since this is a read only talk to the replicas
@get('/db')
def dbexample():
    try:
        conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), user=os.environ.get('PG_USER'),
                                host=os.environ.get('REPLICA_SERVICE_HOST'), password=os.environ.get('PG_PASSWORD'))
    except:
        print(os.environ.get('REPLICA_SERVICE_HOST'))

    cur = conn.cursor()
    # cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints limit 10""")
    cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints ORDER by parkid DESC LIMIT 10""")

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "</h3>"

    cur.close()
    conn.close()

    return result_string


@post('/db')
def dbpost():
    # changes these to the master
    try:
        conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), user=os.environ.get('PG_USER'),
                                host=os.environ.get('MASTER_SERVICE_HOST'), password=os.environ.get('PG_PASSWORD'))
    except:
        print(os.environ.get('MASTER_SERVICE_HOST'))

    # generate a random lat, lon, and place name
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    rw = RandomWords()
    name = rw.random_word() + " " + rw.random_word()

    sql_string = """insert into parkpoints(name, the_geom) values ('""" + name + """', ST_GeomFromText('POINT("""
    sql_string = sql_string + str(lon) + " " + str(lat) + ")', 4326));"

    cur = conn.cursor()
    # I know not this is not good form but I couldn't get it to work with the SRID stuff - probably just being lazy
    cur.execute(sql_string)

    conn.commit()

    # now let's get back our data we just put in
    cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints ORDER by parkid DESC LIMIT 10""")

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "</h3>"

    cur.close()
    conn.close()
    return result_string


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)

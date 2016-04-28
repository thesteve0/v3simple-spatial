__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, DEBUG
import os



@route('/')
def index():
	return "<h1> hello OpenShift Ninja without DB</h1>"

# since this is a read only talk to the replicas
@get('/db')
def dbexample():
	print(os.environ.get('POSTGRESQL_USER'))
	print("After Env")
	try:
		conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), user=os.environ.get('PG_USER'), host=os.environ.get('PG_SLAVE_RC_SERVICE_HOST'), password=os.environ.get('PG_PASSWORD'))
	except:
		print(os.environ.get('PG_USER')	+ "  " + os.environ.get('PG_SLAVE_RC_SERVICE_HOST'))
	
	cur = conn.cursor()
	cur.execute("""SELECT * from pg_user""")
	
	rows = cur.fetchall()
	result_string = "<h2>Here are your results: </h2>"
	for row in rows:
		result_string += "<h3>" + row[0] + "</h3>"

	return  result_string

if __name__ == '__main__':
	run(host='0.0.0.0', port=8080, debug=True)

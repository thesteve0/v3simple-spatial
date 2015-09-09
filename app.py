__author__ = 'spousty'

import psycopg2
from bottle import route, run, DEBUG
import os



@route('/')
def index():
	return "<h1> hello OpenShift Ninja with DB</h1>"

@route('/db')
def dbexample():
	print(os.environ.get('POSTGRESQL_USER'))
	print("After Env")
	try:
		#TODO change the connection info to env variables
		conn = psycopg2.connect(database='db', user=os.environ.get('POSTGRESQL_USER'), host=os.environ.get('POSTGRESQL_92_CENTOS7_SERVICE_HOST'), password=os.environ.get('POSTGRESQL_PASSWORD'))
	except:
		print( os.environ.get('POSTGRESQL_USER') + "  " + os.environ.get('POSTGRESQL_92_CENTOS7_SERVICE_HOST'))
	
	cur = conn.cursor()
	cur.execute("""SELECT * from pg_user""")
	
	rows = cur.fetchall()
	result_string = "<h2>Here are your results: </h2>"
	for row in rows:
		result_string += "<h3>" + row[0] + "</h3>"

	return  result_string

if __name__ == '__main__':
	run(host='0.0.0.0', port=8080, debug=True)

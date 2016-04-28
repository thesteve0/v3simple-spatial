__author__ = 'spousty'

from bottle import route, run, DEBUG
import os



@route('/')
def index():
	return "<h1> hello OpenShift Ninja without DB</h1>"

if __name__ == '__main__':
	run(host='0.0.0.0', port=8080, debug=True)

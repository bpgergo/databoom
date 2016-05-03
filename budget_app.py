from bottle import default_app, route, run, template, redirect, request
from db import *
import logging
from bottle import response

@route('/functions')
def funcs():
    response.content_type='application/json'
    return json.dumps([json_func(f) for f in get_all_funcs()])


@route('/economies')
def econs():
    response.content_type='application/json'
    return json.dumps([json_default(f) for f in get_all_econ()])


@route('/organizations')
def orgs():
    response.content_type='application/json'
    return json.dumps([json_default(f) for f in get_all_org()])



@route('/budget')
def budgets():
    response.content_type='application/json'
    #return [dict(b) for b in get_all_budget()]
    return json.dumps([json_budget(f) for f in get_all_budget()])


application = default_app()
logging.basicConfig(level=logging.DEBUG)

#this will be used when running on your own machine
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run(application, debug=True, reload=True, host="localhost")

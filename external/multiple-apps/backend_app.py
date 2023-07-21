from flask import Flask, render_template, request

backendapp = Flask(__name__)


@backendapp.route('/')
def home():
    msg = "Backend app"
    return '<html><body><h1><i>{}</i></h1></body></html>'.format(msg)


@backendapp.route('/add_backend', methods=['GET'])
def add():

    n1 = int(request.form.get('n1'))
    n2 = int(request.form.get('n2'))

    answer = n1 + n2
    return {'answer': answer}

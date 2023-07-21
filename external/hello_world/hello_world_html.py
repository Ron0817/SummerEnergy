from flask import Flask

app = Flask(__name__)


@app.route('/ece1779')
def hello_world_html():
    msg = "Hello ECE 1779 Students :)"

    return '<html><body><h1>{}</h1></body></html>'.format(msg)


@app.route('/welcome')
def hello_world_html_welcome():
    msg = "Welcome Page."

    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')

    return '<html><body><h1>{}</h1></body></html>'.format(msg)


app.run('0.0.0.0', 5000, debug=True)


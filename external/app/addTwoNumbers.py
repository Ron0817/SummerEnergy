from flask import render_template, request
from app import webapp


@webapp.route('/add', methods=['GET'])
def add():

    if 'n1' not in request.args or 'n2' not in request.args:
        return "Missing arguments."

    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))

    html = """
        <!DOCTYPE html>
        <head>
            <title>Add 2 Numbers</title>
        </head>
            <body>
                {0} + {1} = {2}
            </body>
        </html>
        """
    return html.format(n1, n2, n1 + n2)


@webapp.route('/add_form', methods=['GET', 'POST'])
def add_form():
    html = """
        <!DOCTYPE html>
        <head>
            <title>Add 2 Numbers</title>
        </head>
        <body>
            <form method='get' action='/add'>
                <label>N1</label>
                    <input type='text' name='n1'>
                <label>N2</label>
                    <input type='text' name='n2'>
                <input type='submit' value='Add'>
            </form>
        </body>
    </html>
    """
    return html

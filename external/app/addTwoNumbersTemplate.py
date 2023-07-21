from flask import render_template, request
from app import webapp


@webapp.route('/add_template', methods=['GET', 'POST'])
def add_template():
    if 'n1' not in request.args or 'n2' not in request.args:
        return "Missing arguments."

    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    # n1 = int(request.form['n1'])
    # n2 = int(request.form['n2'])
    print(n1, n2)

    return render_template("add.html", n1=n1, n2=n2, result=n1 + n2)


@webapp.route('/add_form_template', methods=['GET', 'POST'])
def add_form_template():
    return render_template("add_form.html")

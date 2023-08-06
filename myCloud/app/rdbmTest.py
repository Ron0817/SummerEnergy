from flask import render_template, url_for, request, redirect, flash, session
from markupsafe import escape
# from __init__ import app

import mysql.connector

# @app.route('/trivial',methods=['GET'])
# Display an HTML list of all product.
def trivial():
    cnx = mysql.connector.connect(user='ece1779', 
                                  password='12345678',
                                  host='127.0.0.1',
                                  database='estore')

    cursor = cnx.cursor()
    query = "SELECT * FROM customer where id = %s"
    cursor.execute(query,(1,))
    # view = render_template("trivial.html",title="Customer Table", cursor=cursor)
    cnx.close()
    print(cursor)
    return 0

view = trivial()
from flask import render_template, session
from app import webapp

#
# code sample for random key generation
#
# import os
# >>> os.urandom(24)
# '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'


@webapp.route('/count', methods=['GET', 'POST'])
def count():
    numtimes = 0

    if 'numtimes' in session:
        numtimes = session['numtimes']

    session['numtimes'] = numtimes + 1
    session.permanent = True

    return render_template("count.html", numtimes=numtimes)

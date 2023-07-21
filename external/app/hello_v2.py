from app import webapp


@webapp.route('/hello')
def hello():
    return 'Hello, World!'

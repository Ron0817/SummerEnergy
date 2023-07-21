from flask import Flask

global memcache
memcache = {}

app = Flask(__name__)
app.secret_key = 'myCloudSuperSecretKey'

from app import routes


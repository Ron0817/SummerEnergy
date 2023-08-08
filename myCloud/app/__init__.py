from flask import Flask
from app.memcache import Memcache

global memcache
memcache = Memcache()
app = Flask(__name__)
app.secret_key = 'myCloudSuperSecretKey'

from app import routes


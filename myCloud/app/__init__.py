from flask import Flask
from app.memcache import Memcache

# global memcache
memcache = Memcache(capacity=10, replacement_policy="Random")
app = Flask(__name__)
app.secret_key = 'myCloudSuperSecretKey'

from app import routes
from app import threads


from flask import Flask

global memcache
memcache = {}

app = Flask(__name__)

from app import routes


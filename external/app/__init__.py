

from flask import Flask

webapp = Flask(__name__)

from app import main
from app import hello_v2
from app import addTwoNumbers
from app import addTwoNumbersTemplate
from app import count





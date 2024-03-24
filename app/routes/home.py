# app/routes/home.py

from flask import Blueprint, render_template, Flask
from flask_cors import CORS

bp = Blueprint('home', __name__)

app = Flask(__name__)
CORS(app)

@bp.route('/')
def index():
    return render_template('index.html')

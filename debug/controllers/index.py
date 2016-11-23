from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

index_page = Blueprint('index_page', __name__)
db = None


class IndexController(object):
    def __init__(self, database):
        global db
        db = database


@index_page.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# left for testing purposes
@index_page.route('/hello/')
@index_page.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

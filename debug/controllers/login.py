from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

login_page = Blueprint('login_page', __name__)
db = None


class LoginController(object):
    def __init__(self, database):
        global db
        db = database



@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        check = db.verifyUsers(username,password)
        print(check)
        if check:
            # session[username]=request.form[username]
            return redirect(url_for('admin_page.index'))
    return '''
    <form action="" method="post">
        <p><input type=text name=username>
        <p><input type=password name=password>
        <p><input type=submit value=Login>
    </form>
           '''
# use the db to verify the credentials
        # if successful, issue session and redirect to admin page
        # if fail, return error page
        
    # if get request return login page template
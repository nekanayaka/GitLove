"""
Programmer: Nimna Ekanayaka
Date: June 1, 2016
Purpose: Git Service Provider
"""
import os
import sys
from flask import *
from functools import wraps
from flaskext.mysql import MySQL
# from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'nimna'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'gitlove'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# reload(sys)
# sys.setdefaultencoding("utf-8")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please sign in!')
            return redirect(url_for('index'))
    return wrap
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    return render_template('sign_in.html')
    
@app.route('/login_action', methods=['POST'])
def login_action():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM users WHERE `username` = '%s' and `password` = '%s'" % (username, password))
    data = cursor.fetchone()
    if data is None:
        return "Username or password is wrong."
    else:
        session['logged_in'] = True
        return "Login sucessful!"

@app.route('/sign_up', methods=['POST'])
def sign_up():
    return render_template('sign_up.html')
    
@app.route('/sign_up_action', methods=['POST'])
def sign_up_action():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password == confirm_password:
        cursor = mysql.connect().cursor()
        cursor.execute("INSERT INTO users (`username`, `email`, `password`) VALUES ('%s', '%s', '%s')" % (username, email, password))
        mysql.connect().commit()
        print "Profile created successfully."
    else:
        print "Passwords don't match."
    return render_template('index.html')
            

app.run(host = os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)), debug = True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)

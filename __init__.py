"""
Programmer: Nimna Ekanayaka
Date: June 1, 2016
Purpose: Git Service Provider
"""
import os
import sys
import hashlib
from flask import *
from functools import wraps
from flask_mysqldb import MySQL
# from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'db69d2075d3a384312be02455847cd95dda8a37c538d1541'

app.config['MYSQL_USER'] = 'nimna'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gitlove'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

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
    if 'logged_in' in session:
        login_status = True
    else:
        login_status = False
    username = ''
    if 'username' in session:
        username = session['username']
    return render_template('index.html', login_status=login_status, username=username)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    return render_template('sign_in.html')
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE `username` = '%s' and `password` = SHA1('%s')" % (escape(username), escape(password)))
    data = cursor.fetchone()
    if data is None:
        error = "Username or password is wrong."
    else:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('profile', username=username))
    return render_template('sign_in.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    return render_template('sign_up.html')
    
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password_hash = hashlib.sha1(request.form['password'])
    password = password_hash.hexdigest()
    confirm_password_hash = hashlib.sha1(request.form['confirm_password'])
    confirm_password = confirm_password_hash.hexdigest()
    if password == confirm_password:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (`name`, `username`, `email`, `password`) VALUES ('%s', '%s', '%s', '%s')" % (escape(name), escape(username), escape(email), escape(password)))
        mysql.connection.commit()
        success =  "Profile created successfully."
        return render_template('index.html', success=success)
    else:
        error = "Passwords don't match."
        return render_template('sign_up.html', error=error)


@app.route('/profile/<username>', methods=['GET','POST'])
def profile(username):
    return render_template('profile.html', username=username)
            

# app.run(host = os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)), debug = True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)

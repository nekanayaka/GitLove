"""
Programmer: Nimna Ekanayaka
Date: June 1, 2016
Purpose: Git Service Provider
"""
import os
import sys
from flask import *
from functools import wraps

app = Flask(__name__)

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
    
app.run(host = os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)), debug = True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)

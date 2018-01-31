import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , thrills.py

# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'thrills.db'),
#     SECRET_KEY='&@#development_@#$key',
#     USERNAME='admin',
#     PASSWORD='Luwamide123'
# ))
DATABASE = os.path.join(app.root_path, "thrills.db")
app.config['SECRET_KEY'] = '&@#development_@#$key!'
Bootstrap(app)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(15), unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(25))
    win_id = db.Column(db.String(50), unique=True)
    country = db.Column(db.String(60))
    referral = db.Column(db.String(15))

class entries_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True,
    usr_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    req_type = db.Column(db.Integer(1))
    date_of_post = db.Column(db.String(50))
    max_amount = db.Column(db.Float(20))
    min_amount = db.Column(db.Float(20))

class trans_tbl(db.Model):
    trans_id = db.Column(db.Integer, primary_key=True, unique=True)
    usr_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_of_post = db.Column(db.String(50))
     = db.Column(db.String(80))
    status = db.Column(db.Integer(1))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])



# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')
#
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/show_entries')
# def show_entries():
#     # if not session.get('logged_in'):
#     #     error = 'You are NOT logged in'
#     #     result = render_template('login.html', error=error)
#     # else:
#     # db = get_db()
#     cur = db.execute('select username, title, text from entries order by id desc')
#     entries = cur.fetchall()
#     return render_template('show_entries.html', entries=entries)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)
#
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @app.route('/add', methods=['POST'])
# def add_entry():
#     result = None
#     if not session.get('logged_in'):
#         abort(401)
#     else:
#         if request.form['title'] == '' or request.form['text'] == '':
#             flash('Title or Text cannot be empty')
#             result = redirect(url_for('show_entries'))
#         else:
#             result = redirect(url_for('show_entries'))
#             # db = get_db()
#             username = app.config['USERNAME']
#             db.execute('insert into entries (title, text, username) values (?, ?, ?)',
#                  [request.form['title'], request.form['text'], username])
#             db.commit()
#             flash('New entry was successfully posted')
#         return result

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    # if request.method == 'POST':
    #     if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
    #        error = 'Invalid Login Details'
    #     #elif request.form['password'] != app.config['PASSWORD']:
    #      #  error = 'Invalid password'
    #     else:
    #         session['logged_in'] = True
    #         flash('You were logged in')
    #         return redirect(url_for('show_entries'))
    return render_template('login.html', form=form)
#
# @app.route('/logout')
# def logout():
#     #error = "You're not logged In"
#     session['logged_in'] = False
#     flash("You've been logged Out")
#     return render_template('login.html')

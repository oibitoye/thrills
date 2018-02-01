import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


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
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(15), unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    win_username = db.Column(db.String(20), unique=True)
    country = db.Column(db.String(60))
    referrer_id = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class entries_tbl(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    req_type = db.Column(db.Integer)
    date_of_post = db.Column(db.String(50))
    max_amount = db.Column(db.Integer)
    min_amount = db.Column(db.Integer)

class trans_tbl(db.Model):
    trans_id = db.Column(db.Integer, primary_key=True, unique=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_of_trans = db.Column(db.String(50))
    amount_bought= db.Column(db.Integer)
    amount_sold = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    status = db.Column(db.Integer)
    payment_confirm = db.Column(db.Integer)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email address'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    win_username = StringField('Winthrills Username', validators=[InputRequired(), Length(min=4, max=15)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators=[InputRequired(), Length(min=2)])
    referrer_id = StringField('Refeerer\'s Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    password_verify = PasswordField('Verify password', validators=[InputRequired(), EqualTo('password', message='Password must match') , Length(min=8, max=20)])




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

@app.route('/show_entries')
@login_required
def show_entries():
    # if not session.get('logged_in'):
    #     error = 'You are NOT logged in'
    #     result = render_template('login.html', error=error)
    # else:
    # db = get_db()
    # cur = db.execute('select username, title, text from entries order by id desc')
    # entries = cur.fetchall()
    return render_template('show_entries.html')#, entries=entries)

@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    result = None
    # if not session.get('logged_in'):
    #     abort(401)
    # else:
    if request.form['title'] == '' or request.form['text'] == '':
        flash('Title or Text cannot be empty')
        result = redirect(url_for('show_entries'))
    else:
        result = redirect(url_for('show_entries'))
        # db = get_db()
        new_post = entries_tbl(username=form.username.data, email=form.email.data, password=hashed_password, win_username=form.win_username.data, first_name=form.first_name.data, last_name=form.last_name.data, country=form.country.data)
        db.session.add(new_user)
        db.session.commit()
        username = app.config['USERNAME']
        db.execute('insert into entries (title, text, username) values (?, ?, ?)',
             [request.form['title'], request.form['text'], username])
        db.commit()
        flash('New entry was successfully posted')
    return result

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    result = None
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        error = "User already exists"
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        name = User.query.filter_by(username=form.username.data).first()
        mail = User.query.filter_by(email=form.email.data).first()
        # ref_id = User.query.filter_by
        winth = User.query.filter_by(win_username=form.win_username.data).first()
        if name or mail or winth:
            result = render_template('signup.html', form=form)
        else:
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, win_username=form.win_username.data, first_name=form.first_name.data, last_name=form.last_name.data, country=form.country.data)
            db.session.add(new_user)
            db.session.commit()
            flash('New user has been created!')
            result =  "<h1>New user has been created!</h1>"
            #result = render_template('login.html', form=form)
            return result
    return render_template('signup.html', form=form)
    #return result
#
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                if form.username.data == 'admin':
                    login_user(user, remember=form.remember.data)
                    result = redirect(url_for('dashboard'))
                else:
                    login_user(user, remember=form.remember.data)
                    result = redirect(url_for('show_entries'))
                return result


        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
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
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
#
# @app.route('/logout')
# def logout():
#     #error = "You're not logged In"
#     session['logged_in'] = False
#     flash("You've been logged Out")
#     return render_template('login.html')

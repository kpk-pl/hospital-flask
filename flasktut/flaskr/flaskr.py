import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskr_db import *     
     
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()    
        
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()    
    
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)    
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select r.name from users as u join rights as r on r.id = u.rights where u.login = ? and u.password = ?', [request.form['username'], request.form['password']])
        res = cur.fetchone()
        if res:
            session['logged_in'] = True
            session['username'] = request.form['username']
            session['rights'] = res[0]
            flash('Hello ' + request.form['username'])
            return redirect(url_for('show_entries'))
        else:
            error = 'Incorrect username or password'
    return render_template('login.html', error=error)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        db = get_db()
        # first find role id
        cur = db.execute('select id from rights where name = \'client\'')
        if cur:
            id = cur.fetchone()[0]
            #check if user or email already exists
            cur = db.execute('select count(*) from users where login = ? or email = ?', [request.form['username'], request.form['email']])
            if cur:
                entry = cur.fetchone()
                if entry[0] == 0: 
                    db.execute('insert into users (rights, login, password, first_name, last_name, date_registered, address, postal_code, city, telephone, email) values (?, ?, ?, ?, ?, date(\'now\'), ?, ?, ?, ?, ?)', [id,request.form['username'], request.form['password'], request.form['first_name'], request.form['last_name'], request.form['address'], request.form['postal'], request.form['city'], request.form['phone'], request.form['email']])
                    db.commit()
                    flash('Registered successfully. Now you can log in!')
                    return redirect(url_for('show_entries'))
                else:
                    error = 'User with this name or email already exists. Select another username or email.'
            else:
                error = 'Internal database error.'
        else:
            error = 'Internal database error.'
    return render_template('register.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('rights', None)
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('show_entries'))
    
@app.route('/my_account')
def my_account():
    error = None
    db = get_db()
    info = get_user_info(db, session['username'])
    if not info:
        error = 'No such user in database'
    return render_template('my_account.html', error=error, info=info)
    
@app.route('/edit_my_account', methods=['GET', 'POST'])
def edit_my_account():
    error = None
    db = get_db()
    info = get_user_info(db, session['username'])
    if request.method == 'POST':
        if request.form['email'] == info['email'] or not email_exists(db,request.form['email']):
            db.execute('update users set first_name = ?, last_name = ?, email = ?, address = ?, city = ?, postal_code = ?, telephone = ? where login = ?', [request.form['first_name'], request.form['last_name'], request.form['email'], request.form['address'], request.form['city'], request.form['postal'], request.form['phone'], session['username']])
            db.commit()
            flash('Personal information changed successfully')
            return redirect(url_for('my_account'))
        else:
            error = 'User with that email address already exists'
    if not info:
        error = 'No such user in database'    
    return render_template('edit_my_account.html', error=error, info=info)
    
def validate_rights(right):
    if 'rights' not in session or session['rights'] != rights:
        return False
    return True
    
@app.route('/control_panel')
def control_panel():
    if not validate_rights('admin'):
        return redirect('/')
    return render_template('control_panel.html')
    
@app.route('/cp_user_db')
def cp_user_db():
    if not validate_rights('admin'):
        return redirect('/')
    users = get_all_users_info(get_db())
    return render_template('cp_user_db.html', users=users)    
    
if __name__ == '__main__':
    app.run()
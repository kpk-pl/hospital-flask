import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
     
from tools import *
     
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
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
    
@app.route('/', methods=['GET'])
def main_screen():
    db = get_db()
    if 'logged_in' in session and session['logged_in']:
        position = get_position(db, session['username'])
    else:
        position = None
     
    if position == 'Admin':
        return render_template('admin_main.html', position=position)
    elif position == "Receptionist":
        return render_template('receptionist_main.html', position=position)
        
    return render_template('main_screen.html', position=position)    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'logged_in' in session and session['logged_in']:
        flash('You are already logged in as ' + session['username'])
        return redirect(url_for('main_screen'))
        
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select count(*) from employees where login = ? and password = ?', [request.form['login'], request.form['password']])
        res = cur.fetchone()
        if res:
            session['logged_in'] = True
            session['username'] = request.form['login']
            flash('Hello ' + request.form['login'])
            return redirect(url_for('main_screen'))
        else:
            error = 'Incorrect username or password'
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('main_screen'))
    
@app.route('/my_account')
def my_account():
    if 'logged_in' not in session or not session['logged_in']:
        flash('You were not logged in')
        return redirect(url_for('main_screen'))
        
    db = get_db()
    cur = db.execute('select e.login, e.fname, e.lname, p.name as position, e.salary from employees as e join positions as p on e.position_id = p.id where e.login = ?', [session['username']])
    res = cur.fetchone()
    if not res:
        flash('Error accessing database')
        
    return render_template('my_account.html', data=res)
    
@app.route('/view_all_databases')
def view_all_databases():
    db = get_db()
    if 'logged_in' not in session or not session['logged_in'] or get_position(db, session['username']) != 'Admin':
        flash('You do not have rights to access this part of website')
        return redirect(url_for('main_screen'))    
        
    emps = db.execute('select * from employees').fetchall()
    pos = db.execute('select * from positions').fetchall()
    pat = db.execute('select * from patients').fetchall()
    fil = db.execute('select * from files').fetchall()
      
    return render_template('view_all_databases.html', employees=emps, positions=pos, patients=pat, files=fil)
    
@app.route('/sign_in_new_patient', methods=['GET', 'POST'])
def sign_in_new_patient():
    error = None
    db = get_db()
    if 'logged_in' not in session or not session['logged_in'] or get_position(db, session['username']) not in ['Admin', 'Receptionist']:
        flash('You do not have rights to access this part of website')
        return redirect(url_for('main_screen'))    

    form_data = {'fname':'', 'lname':'', 'pesel':'', 'dbirth':''}         
    if request.method == 'POST':
        if request.form['fname'] == '' and request.form['lname'] == '' and request.form['dbirth'] == '':
            cur = db.execute('select fname, lname, birth from patients where pesel = ?', [request.form['pesel']])
            patient = cur.fetchone()
            if patient:
                form_data['fname'] = patient[0]
                form_data['lname'] = patient[1]
                form_data['pesel'] = request.form['pesel']
                form_data['dbirth'] = patient[2]
                flash('Please confirm this data!')
            else:
                error = 'Patient with this PESEL does not exist'
        else:
            cur = db.execute('select count(*) from patients where pesel = ?', [request.form['pesel']])
            if cur.fetchone()[0] == 0:
                if request.form['fname'] != '' and request.form['lname'] != '' and len(request.form['pesel']) == 11:
                    try:
                        cur = db.execute('insert into patients (fname, lname, pesel, birth) values (?, ?, ?, date(?))', [request.form['fname'],request.form['lname'],request.form['pesel'],request.form['dbirth']])
                        db.commit()
                    except:
                        error = "Incorrect data format"
                    else:
                        flash('Patient successfully added')
                else:
                    error = "Incorrect data"
            if not error:
                if not patient_signed_in(db, request.form['pesel']):
                    db.execute('insert into files (patient_pesel, admission_d) values (?, date(\'now\'))', [request.form['pesel']])
                    db.commit()
                    flash('Patient signed in')
                    return redirect(url_for('main_screen'))
                else:
                    error = "Patient already signed in"
    return render_template('sign_in_new_patient.html', data=form_data, error=error)
    
if __name__ == '__main__':
    app.run()
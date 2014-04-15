def get_user_info(db, user):
    cur = db.execute('select first_name, last_name, address, postal_code, city, email, telephone from users where login = ?', [user])
    return cur.fetchone()
    
def get_all_users_info(db):
    cur = db.execute('select * from users')
    return cur.fetchall()
    
def email_exists(db, email):
    cur = db.execute('select count(*) from users where email = ?', [email])    
    return cur.fetchone()[0] == 1
    
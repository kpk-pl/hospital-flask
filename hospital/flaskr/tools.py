def get_position(db, user):
    cur = db.execute('select p.name from employees as e join positions as p on e.position_id = p.id where e.login = ?', [user])
    res = cur.fetchone()
    return res[0] if res else None
    
def patient_signed_in(db, pesel):
    cur = db.execute('select count(*) from files where patient_pesel = ? and discharge_d is null', [pesel])
    res = cur.fetchone()
    return True if res[0] > 0 else False
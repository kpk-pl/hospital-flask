def get_position(db, user):
    cur = db.execute('select p.name from employees as e join positions as p on e.position_id = p.id where e.login = ?', [user])
    res = cur.fetchone()
    return res[0] if res else None
    
def patient_signed_in(db, pesel):
    cur = db.execute('select count(*) from files where patient_pesel = ? and discharge_d is null', [pesel])
    res = cur.fetchone()
    return True if res[0] > 0 else False
    
def get_patients_allowed(db, username):
    cur = db.execute('select p.fname, p.lname, p.pesel, f.admission_d from patients p join files f on p.pesel = f.patient_pesel join assignments a on a.fil_id = f.id join employees e on e.id = a.employee_id where e.login = ? and f.discharge_d is null', [username])
    return cur.fetchall()    
    
def get_patient_details_if_allowed(db, username, pesel):
    cur = db.execute('select p.fname, p.lname, p.pesel, f.admission_d from patients p join files f on p.pesel = f.patient_pesel join assignments a on a.fil_id = f.id join employees e on e.id = a.employee_id where e.login = ? and f.discharge_d is null and p.pesel = ?', [username, pesel])    
    return cur.fetchone()
    
    
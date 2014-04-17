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
    
def get_patient_details(db, pesel):
    return db.execute('select p.fname, p.lname, p.pesel, f.admission_d from files f join patients p on f.patient_pesel = p.pesel where f.discharge_d is null and p.pesel = ?', [pesel]).fetchone()
    
def get_assigned_personel_for_patient(db, pesel):
    cur = db.execute('select e.fname, e.lname, p.name, e.rights from employees e join positions p on p.id = e.position_id join assignments a on a.employee_id = e.id join files f on f.id = a.fil_id join patients pat on f.patient_pesel = pat.pesel where pat.pesel = ? and f.discharge_d is null order by e.rights desc', [pesel])
    return cur.fetchall()
    
def get_all_medical_personel(db):
    cur = db.execute('select e.fname || " " || e.lname || " (" || p.name || ")", e.id from employees e join positions p on p.id = e.position_id where p.name in ("Nurse", "Doctor", "Head physician")')
    return cur.fetchall()
    
def add_assignment(db, pesel, employee_id):
    db.execute('begin transaction')
    cur = db.execute('select count(*) from assignments a join files f on f.id = a.fil_id where f.patient_pesel = ? and a.employee_id = ? and f.discharge_d is null', [pesel, employee_id])
    if cur.fetchone()[0] == 0:
        db.execute('insert into assignments (fil_id, employee_id) values ((select id from files where patient_pesel = ? and discharge_d is null),(select id from employees where id = ?))', [pesel, employee_id])
        db.commit()
        return True
    else:
        db.rollback()
        return False
    
def is_assigned(db, pesel, username):
    cur = db.execute('select count(*) from assignments a join employees e on e.id = a.employee_id join files f on f.id = a.fil_id where f.discharge_d is null and f.patient_pesel = ? and e.login = ?', [pesel, username])
    res = cur.fetchone()
    return True if res[0] > 0 else False
    
def remove_assignment(db, pesel, username):
    cur = db.execute('delete from assignments where fil_id = (select id from files where discharge_d is null and patient_pesel = ?) and employee_id = (select id from employees where login = ?)', [pesel, username])
    db.commit()
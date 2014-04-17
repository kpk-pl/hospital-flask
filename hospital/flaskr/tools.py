def get_position(db, user):
    cur = db.execute('select p.name from employees as e join positions as p on e.position_id = p.id where e.login = ?', [user])
    res = cur.fetchone()
    return res[0] if res else None

def get_patient_info(db, pesel):
    return db.execute('select fname, lname from patients where pesel = ?', [pesel]).fetchone()

def add_new_patient(db, fname, lname, pesel):
    """
    Tries to add new patient to database
    Error codes:
    -1: fname empty
    -2: lname empty
    -3: pesel malformed
    if ok returns positive number
    if patient already existed returns 0
    """
    first_name = fname.strip()
    last_name = lname.strip()
    pesel = int(pesel)
    if len(first_name) == 0:
        return -1
    if len(last_name) == 0:
        return -2
    if len(str(pesel)) != 11:
        return -3
    try:
        db.execute('insert into patients (fname, lname, pesel) values (?, ?, ?)', [first_name, last_name, pesel])
    except:
        return 0
    else:
        db.commit()
    return 1
    
def patient_signed_in(db, pesel):
    cur = db.execute('select count(*) from files where patient_pesel = ? and discharge_d is null', [pesel])
    res = cur.fetchone()
    return True if res[0] > 0 else False
 
def register_patient(db, fname, lname, pesel):
    """
    Registers patient in hospital
    Patient must be already added to database
    Error codes:
    -1: Patient's info does not match
    -2: Patient already in hospital
    -3: Patient not exists
    On success returns positive number
    """
    first_name = fname.strip()
    last_name = lname.strip()
    pesel = int(pesel)
    errcode = 0
    db.execute('begin transaction')
    info = get_patient_info(db, pesel)
    if info:
        if info[0] == first_name and info[1] == last_name:
            if not patient_signed_in(db, pesel):
                db.execute('insert into files (patient_pesel, admission_d) values (?, datetime(\'now\'))', [pesel])
                db.commit()
                return 1
            else:
                errcode = -2
        else:
            errcode = -1
    else:
        errcode = -3
    db.rollback()
    return errcode
 
def get_employee_id(db, username):
    id = db.execute('select id from employees where login = ?', [username]).fetchone()
    return id[0] if id else None
    
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
    
def get_current_history(db, pesel):
    cur = db.execute("select h.entry_d, d.name, h.drug_quantity || u.name, pr.name, e.fname || ' ' || e.lname || ' (' || p.name || ')' from history h join files f on f.id = h.fil_id join employees e on e.id = h.employee_id join positions p on p.id = e.position_id left join drugs d on d.id = h.drug_id left join units u on d.unit_id = u.id left join procedures pr on pr.id = h.procedure_id where f.patient_pesel = ? and f.discharge_d is null order by h.entry_d desc", [pesel])
    return cur.fetchall()
    
def get_all_allowed_drugs(db, username):
    return db.execute("select d.id, d.name || ' [' || d.price || '$/' || u.name || ']' from drugs d join units u on d.unit_id = u.id where d.min_rights <= (select rights from employees where login = ?) order by d.name", [username]).fetchall()
    
def get_all_allowed_procedures(db, username):
    return db.execute("select p.id, p.name || ' [' || p.price || '$]' from procedures p where p.min_rights <= (select rights from employees where login = ?) order by p.name", [username]).fetchall()    
    
def prescribe_drug(db, username, pesel, drug_id, quantity):
    """
    Prescribes drug for specified patient pesel
    Error conditions:
    username not in database: -1
    pesel not in hospital: -2
    employee not assigned to pesel: -3
    drug does not exist: -4
    employee not allowed to prescribe the drug: -5
    If all good returns quantity
    If there is not enough returns how much there is
    """
    errcode = 0
    db.execute('begin transaction')
    employee_id = get_employee_id(db, username)
    if employee_id:
        # find file id for the pesel - this verifies that pesel is in hospital
        file_id = db.execute('select id from files where patient_pesel = ? and discharge_d is null', [pesel]).fetchone()
        if file_id:
            file_id = file_id[0]
            # verify that employee is assigned to pesel
            if db.execute('select count(*) from assignments where fil_id = ? and employee_id = ?', [file_id, employee_id]).fetchone()[0] > 0:
                #check if drug exists
                if db.execute('select count(*) from drugs where id = ?', [drug_id]).fetchone()[0] == 1:
                    #check that employee is allowed to prescribe the drug
                    drug_q = db.execute('select quantity from drugs where id = ? and min_rights <= (select rights from employees where id = ?)', [drug_id, employee_id]).fetchone()
                    if drug_q:
                        drug_q = drug_q[0]
                        #check if there is enough to prescribe
                        if drug_q >= quantity:
                            db.execute('update drugs set quantity = ? where id = ?', [drug_q - quantity, drug_id])
                            db.execute('insert into history (fil_id, entry_d, employee_id, drug_id, drug_quantity) values (?, datetime(\'now\'), ?, ?, ?)', [file_id, employee_id, drug_id, quantity])
                            db.commit()
                            return quantity
                        else:
                            errcode = drug_q
                    else:
                        errcode = -5
                else:
                    errcode = -4
            else:
                errcode = -3
        else:
            errcode = -2
    else:
        errcode = -1
    db.rollback()
    return errcode
  
def order_procedure(db, username, pesel, proc_id):
    """
    Order a procedure for a patient with specified pesel
    Error conditions:
    username not in database: -1
    pesel not in hospital: -2
    employee not assigned to pesel: -3
    procedure does not exist: -4
    employee not allowed to order the procedure: -5    
    if all good, returns positive number
    """
    errcode = 0
    db.execute('begin transaction')
    employee_id = get_employee_id(db, username)
    if employee_id:
        # find file id for the pesel - this verifies that pesel is in hospital
        file_id = db.execute('select id from files where patient_pesel = ? and discharge_d is null', [pesel]).fetchone()
        if file_id:
            file_id = file_id[0]
            # verify that employee is assigned to pesel
            if db.execute('select count(*) from assignments where fil_id = ? and employee_id = ?', [file_id, employee_id]).fetchone()[0] > 0:
                #check if procedure exists
                if db.execute('select count(*) from procedures where id = ?', [proc_id]).fetchone()[0] == 1:
                    #check that employee is allowed to order the procedure
                    if db.execute('select count(*) from procedures where id = ? and min_rights <= (select rights from employees where id = ?)', [proc_id, employee_id]).fetchone()[0] == 1:
                        db.execute('insert into history (fil_id, entry_d, employee_id, procedure_id) values (?, datetime(\'now\'), ?, ?)', [file_id, employee_id, proc_id])
                        db.commit()
                        return 1
                    else:
                        errcode = -5
                else:
                    errcode = -4
            else:
                errcode = -3
        else:
            errcode = -2
    else:
        errcode = -1
    db.rollback()
    return errcode
    
def discharge_patient(db, pesel):
    db.execute('begin transaction')
    file_id = db.execute('select id from files where patient_pesel = ? and discharge_d is null', [pesel]).fetchone()
    if file_id:
        file_id = file_id[0]
        db.execute('update files set discharge_d = datetime(\'now\') where id = ?', [file_id])
        db.execute('delete from assignments where fil_id = ?', [file_id])
        db.commit()
        return True
    db.rollback()
    return False
drop table if exists patients;
create table patients (
    pesel integer primary key,
    fname text not null,
    lname text not null
);

drop table if exists positions;
create table positions (
    id integer primary key autoincrement,
    name text not null
);

drop table if exists employees;
create table employees (
    id integer primary key autoincrement,
    fname text not null,
    lname text not null,
    login text not null unique,
    password text not null,
    position_id integer not null,
    employment_d date not null,
    salary integer not null,
    rights integer not null,
    foreign key(position_id) references positions(id)
);

drop table if exists files;
create table files (
    id integer primary key autoincrement,
    patient_pesel integer not null,
    admission_d datetime not null,
    discharge_d datetime,
    foreign key(patient_pesel) references patients(pesel)
);

drop table if exists units;
create table units (
    id integer primary key autoincrement,
    name text not null
);

drop table if exists drugs;
create table drugs (
    id integer primary key autoincrement,
    name text not null,
    quantity float not null,
    unit_id integer not null,
    price float not null,
    min_rights integer not null,
    active integer not null,
    foreign key(unit_id) references units(id)
);

drop table if exists procedures;
create table procedures (
    id integer primary key autoincrement,
    name text not null,
    price float not null,
    min_rights integer not null,
    active integer not null
);

drop table if exists history;
create table history (
    id integer primary key autoincrement,
    fil_id integer not null,
    entry_d datetime not null,
    employee_id integer not null,
    drug_id integer,
    procedure_id integer,
    drug_quantity float,
    foreign key(fil_id) references files(id),
    foreign key(employee_id) references employees(id),
    foreign key(drug_id) references drugs(id),
    foreign key(procedure_id) references procedures(id)
);

drop table if exists assignments;
create table assignments (
    fil_id integer not null,
    employee_id integer not null,
    foreign key(fil_id) references files(id),
    foreign key(employee_id) references employees(id)
);

drop table if exists orders;
create table orders (
    id integer primary key autoincrement,
    drug_id integer not null,
    quantity float not null,
    unit_price float not null,
    order_d datetime not null,
    employee_id integer not null,
    foreign key(employee_id) references employees(id),
    foreign key(drug_id) references drugs(id)
);

drop trigger if exists remove_assignments_discharge;
create trigger remove_assignments_discharge after update of discharge_d on files
for each row
when old.discharge_d is null and new.discharge_d is not null
begin
    delete from assignments where fil_id = new.id;
end;

insert into positions (id, name) values (0, "Admin");
insert into positions (id, name) values (1, "Receptionist");
insert into positions (id, name) values (2, "Head physician");
insert into positions (id, name) values (3, "Doctor");
insert into positions (id, name) values (4, "Nurse");
insert into positions (id, name) values (5, "Warehouseman");
insert into positions (id, name) values (6, "Accountant");

insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(1,  'Admin',        '',             0,  date('2014-01-15'), 10000,  255,    'admin',        'admin');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(2,  'Jane',         'Strongman',    1,  date('2014-01-19'), 4000,   0,      'receptionist', 'receptionist');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(3,  'Steve',        'Balman',       2,  date('2014-03-18'), 9500,   200,    'chief',        'chief');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(4,  'Jane',         'Doe',          3,  date('2014-04-05'), 7000,   80,     'doctor',       'doctor');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(5,  'Bill',         'Wicked',       3,  date('2014-02-17'), 5000,   35,     'doctor1',      'doctor1');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(6,  'Sarah',        'Nilan',        3,  date('2014-02-18'), 6000,   15,     'doctor2',      'doctor2');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(7,  'Stephanie',    'Miller',       4,  date('2014-03-15'), 3500,   10,     'nurse',        'nurse');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(8,  'Rollo',        'Middleheimer', 5,  date('2014-03-22'), 2000,   0,      'warehouse',    'warehouse');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(9,  'Cate',         'Stachorsky',   6,  date('2014-01-27'), 6750,   0,      'accountant',   'accountant');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(10, 'Bob',          'Pretty',       3,  date('2014-01-17'), 9500,   75,     'doctor3',      'doctor3');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(11, 'Rob',          'Bass',         3,  date('2014-02-27'), 8500,   55,     'doctor4',      'doctor4');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(12, 'Katy',         'Bing',         3,  date('2014-02-02'), 6000,   30,     'doctor5',      'doctor5');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(13, 'Wellma',       'Stander',      4,  date('2014-01-03'), 4500,   13,     'nurse1',       'nurse1');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values 
(14, 'Maggie',       'Wellfare',     4,  date('2013-12-27'), 4000,   7,      'nurse2',       'nurse2');

insert into patients (fname, lname, pesel) values ('Arnold',    'Bow',      12345678911);
insert into patients (fname, lname, pesel) values ('Jonathan',  'Bowman',   31273504732);
insert into patients (fname, lname, pesel) values ('Henry',     'Ford',     45678912355);
insert into patients (fname, lname, pesel) values ('Janete',    'Bellmore', 54785413486);
insert into patients (fname, lname, pesel) values ('Joanne',    'Hellfire', 45217513548);

insert into files (id, patient_pesel, admission_d, discharge_d) values (1, 45217513548, datetime('2014-01-18 12:16:22'), datetime('2014-03-13 08:12:16'));
insert into files (id, patient_pesel, admission_d, discharge_d) values (2, 12345678911, datetime('2014-02-16 12:12:55'), datetime('2014-02-20 06:46:12'));
insert into files (id, patient_pesel, admission_d, discharge_d) values (3, 31273504732, datetime('2014-02-19 05:51:12'), datetime('2014-03-15 09:12:12'));
insert into files (id, patient_pesel, admission_d, discharge_d) values (4, 12345678911, datetime('2014-03-14 23:16:07'), null);
insert into files (id, patient_pesel, admission_d, discharge_d) values (5, 45678912355, datetime('2014-02-16 12:12:35'), null);
insert into files (id, patient_pesel, admission_d, discharge_d) values (6, 54785413486, datetime('2014-03-14 23:16:07'), null);
insert into files (id, patient_pesel, admission_d, discharge_d) values (7, 45217513548, datetime('2014-03-19 01:12:54'), null);

insert into assignments (fil_id, employee_id) values (4, 11);
insert into assignments (fil_id, employee_id) values (4, 5);
insert into assignments (fil_id, employee_id) values (4, 3);
insert into assignments (fil_id, employee_id) values (4, 7);
insert into assignments (fil_id, employee_id) values (5, 11);
insert into assignments (fil_id, employee_id) values (5, 12);
insert into assignments (fil_id, employee_id) values (5, 13);
insert into assignments (fil_id, employee_id) values (6, 6);
insert into assignments (fil_id, employee_id) values (6, 7);
insert into assignments (fil_id, employee_id) values (6, 10);
insert into assignments (fil_id, employee_id) values (6, 3);
insert into assignments (fil_id, employee_id) values (7, 12);
insert into assignments (fil_id, employee_id) values (7, 14);
insert into assignments (fil_id, employee_id) values (7, 13);

insert into units (id, name) values (1, 'pc');
insert into units (id, name) values (2, 'g');
insert into units (id, name) values (3, 'ml');

insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (1, "Aspirin",     100,   1, 0.02,   2,   1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (2, "Ketonal",     10,    3, 2.0,    20,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (3, "Astmodil",    16,    2, 54.0,   30,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (4, "Kandesar",    30.5,  2, 34.4,   40,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (5, "Unibasis",    2.2,   3, 26.71,  4,   1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (6, "Acard",       314,   1, 14.21,  7,   1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (7, "Hascoderm",   27.1,  2, 2.45,   54,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (8, "Plavix",      74,    1, 6.79,   67,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (9, "Kaflex",      4.9,   3, 24.2,   17,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (10,"Quinax",      4,     3, 71.3,   29,  1);
insert into drugs (id, name, quantity, unit_id, price, min_rights, active) values (11,"Talidomid",   120.0, 3, 14.2,   45,  0);
    
insert into procedures (id, name, price, min_rights, active) values (1,  'Brain surgery',   5000.0,     70,     1);
insert into procedures (id, name, price, min_rights, active) values (2,  'Flu shot',        25.0,       15,     1);
insert into procedures (id, name, price, min_rights, active) values (3,  'Bandage',         2.42,       2,      1);
insert into procedures (id, name, price, min_rights, active) values (4,  'MRI',             560.0,      30,     1);
insert into procedures (id, name, price, min_rights, active) values (5,  'Roentgen',        70.0,       20,     1);
insert into procedures (id, name, price, min_rights, active) values (6,  'Stiching',        12.5,       23,     1);
insert into procedures (id, name, price, min_rights, active) values (7,  'Casting',         230.0,      30,     1);
insert into procedures (id, name, price, min_rights, active) values (8,  'Observation',     200.0,      17,     1);
insert into procedures (id, name, price, min_rights, active) values (9,  'Biopsy',          2000.0,     50,     1);
insert into procedures (id, name, price, min_rights, active) values (10, 'Chemotherapy',    4500.0,     60,     1);
insert into procedures (id, name, price, min_rights, active) values (11, 'Blood test',      315.0,      20,     0);

insert into orders (drug_id, quantity, unit_price, order_d, employee_id) values (3, 100.0, 50.0, datetime('2014-02-14 14:19:21'), 8);
insert into orders (drug_id, quantity, unit_price, order_d, employee_id) values (5, 200.0, 26.0, datetime('2014-02-14 14:19:21'), 8);
insert into orders (drug_id, quantity, unit_price, order_d, employee_id) values (6, 300.0, 15.0, datetime('2014-02-14 14:19:21'), 8);

insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(1, datetime('2014-01-22 13:07:22'), 11,   11,      null,   1.0);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(1, datetime('2014-01-23 16:29:13'), 11,   null,    11,     null);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(1, datetime('2014-01-25 21:17:54'), 14,   1,       null,   2.0);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(2, datetime('2014-02-18 12:12:37'), 12,   null,    8,      null);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(2, datetime('2014-02-18 13:47:00'), 12,   null,    5,      null);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(3, datetime('2014-02-22 19:32:42'), 3,    null,    1,      null);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(3, datetime('2014-02-23 03:19:22'), 3,    null,    8,      null);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(3, datetime('2014-02-23 03:20:12'), 3,    2,       null,   0.4);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(4, datetime('2014-03-15 14:56:42'), 5,    9,       6,      0.7);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(5, datetime('2014-02-16 14:18:22'), 13,   6,       null,   10);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(5, datetime('2014-02-17 17:16:13'), 11,   null,    4,      null);
insert into history (fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values 
(7, datetime('2014-03-22 17:18:42'), 13,   null,    3,      null);
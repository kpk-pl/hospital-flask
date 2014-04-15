drop table if exists patients;
create table patients (
    pesel integer primary key,
    fname text not null,
    lname text not null,
    birth date not null
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
    login text not null,
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
    admission_d date not null,
    discharge_d date,
    
    foreign key(patient_pesel) references patients(pesel)
);

drop table if exists drugs;
create table drugs (
    id integer primary key autoincrement,
    name text not null,
    quantity integer not null,
    price integer not null,
    min_rights integer not null
);

drop table if exists procedures;
create table procedures (
    id integer primary key autoincrement,
    name text not null,
    price integer not null,
    min_rights integer not null
);

drop table if exists history;
create table history (
    id integer primary key autoincrement,
    fil_id integer not null,
    entry_d date not null,
    employee_id integer not null,
    drug_id integer,
    procedure_id integer,
    drug_quantity integer,
    
    foreign key(fil_id) references files(id),
    foreign key(employee_id) references employees(id),
    foreign key(drug_id) references drugs(id),
    foreign key(procedure_id) references procedure(id)
);

drop table if exists assignments;
create table assignments (
    procedure_id integer not null,
    employee_id integer not null,
    
    foreign key(procedure_id) references procedures(id),
    foreign key(employee_id) references employees(id)
);

insert into positions (id, name) values (0, "Admin");
insert into positions (id, name) values (1, "Receptionist");
insert into positions (id, name) values (2, "Head physician");

insert into employees (fname, lname, position_id, employment_d, salary, rights, login, password) values ('Admin', '', 0, date('now'), 10000, 255, 'admin', 'admin');
insert into employees (fname, lname, position_id, employment_d, salary, rights, login, password) values ('Jane', 'Strongman', 1, date('now'), 4000, 0, 'receptionist', 'receptionist');
insert into employees (fname, lname, position_id, employment_d, salary, rights, login, password) values ('Steve', 'Balman', 2, date('now'), 9500, 200, 'chief', 'chief');

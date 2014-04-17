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
    foreign key(unit_id) references units(id)
);

drop table if exists procedures;
create table procedures (
    id integer primary key autoincrement,
    name text not null,
    price float not null,
    min_rights integer not null
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

insert into positions (id, name) values (0, "Admin");
insert into positions (id, name) values (1, "Receptionist");
insert into positions (id, name) values (2, "Head physician");
insert into positions (id, name) values (3, "Doctor");
insert into positions (id, name) values (4, "Nurse");
insert into positions (id, name) values (5, "Warehouseman");
insert into positions (id, name) values (6, "Accountant");

insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (1, 'Admin', '', 0, date('now'), 10000, 255, 'admin', 'admin');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (2, 'Jane', 'Strongman', 1, date('now'), 4000, 0, 'receptionist', 'receptionist');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (3, 'Steve', 'Balman', 2, date('now'), 9500, 200, 'chief', 'chief');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (4, 'Jane', 'Doe', 3, date('now'), 7000, 80, 'doctor', 'doctor');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (5, 'Bill', 'Wicked', 3, date('now'), 5000, 35, 'doctor1', 'doctor1');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (6, 'Sarah', 'Nilan', 3, date('now'), 6000, 15, 'doctor2', 'doctor2');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (7, 'Stephanie', 'Miller', 4, date('now'), 3500, 10, 'nurse', 'nurse');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (8, 'Rollo', 'Middleheimer', 5, date('now'), 2000, 0, 'warehouse', 'warehouse');
insert into employees (id, fname, lname, position_id, employment_d, salary, rights, login, password) values (9, 'Cate', 'Stachorsky', 6, date('now'), 6750, 0, 'accountant', 'accountant');

insert into patients (fname, lname, pesel) values ('Arnold', 'Bow', 12345678911);
insert into patients (fname, lname, pesel) values ('Jonathan', 'Bowman', 31273504732);

insert into files (id, patient_pesel, admission_d) values (1, 12345678911, datetime('now'));
insert into files (id, patient_pesel, admission_d) values (2, 31273504732, datetime('now'));

insert into assignments (fil_id, employee_id) values (1, 4);
insert into assignments (fil_id, employee_id) values (1, 5);
insert into assignments (fil_id, employee_id) values (1, 7);
insert into assignments (fil_id, employee_id) values (2, 5);

insert into units (id, name) values (1, 'pc');
insert into units (id, name) values (2, 'g');
insert into units (id, name) values (3, 'ml');
insert into units (id, name) values (4, 'min');

insert into drugs (id, name, quantity, unit_id, price, min_rights) values (1, "Aspirin", 100, 1, 0.02, 2);
insert into drugs (id, name, quantity, unit_id, price, min_rights) values (2, "Ketonal", 10, 3, 2.0, 20);
insert into drugs (id, name, quantity, unit_id, price, min_rights) values (3, "Astmodil", 16, 2, 54.0, 30);
    
insert into procedures (id, name, price, min_rights) values (1, 'Brain surgery', 5000.0, 70);
insert into procedures (id, name, price, min_rights) values (2, 'Flu shot', 25.0, 15);

insert into history (id, fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values (1, 1, datetime('now'), 6, 1, null, 3);
insert into history (id, fil_id, entry_d, employee_id, drug_id, procedure_id, drug_quantity) values (2, 1, datetime('now'), 5, null, 2, null);
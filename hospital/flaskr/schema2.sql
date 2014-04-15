drop table if exists patient;
create table patient (
    pesel integer primary key;
    fname text not null;
    lname text not null;
    birth date not null;
);

drop table if exists positions;
create table positions (
    id integer primary key autoincrement;
    name text not null;
);

drop table if exists employees;
create table employees (
    id integer primary key autoincrement;
    fname text not null;
    lname text not null;
    position integer not null;
    empl_date date not null;
    salary integer not null;
    rights integer not null;
    
    foreign key(position) references positions(id)
);

drop 

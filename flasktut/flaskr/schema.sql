drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists rights;
create table rights (
  id integer primary key autoincrement,
  name text not null
);

insert into rights values (0, 'admin');
insert into rights values (1, 'salesman');
insert into rights values (2, 'client');

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  rights integer not null,
  login text not null,
  password text not null,
  first_name text not null,
  last_name text not null,
  date_registered date not null,
  address text not null,
  postal_code text not null,
  city text not null,
  telephone text not null,
  email text not null,
  
  foreign key(rights) references rights(id)
);

insert into users values (
  0, 0, 'admin', 'admin', 'Krzysztof', 'Kapusta', 'now', 'Sienna 24', '31-452', 'Kraków', '123456789', 'admin@admin.com'
);
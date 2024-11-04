create schema baby_login;

create user 'baby_login' identified by 'baby_login';

grant select on baby_login.* to 'baby_login' with grant option;

create table baby_login.users
(
    username varchar(256) primary key,
    password varchar(256)
);

insert into baby_login.users (username, password) values ('admin', 'dummy_password');

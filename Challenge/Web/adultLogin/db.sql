create schema adult_login;

create user 'adult_login' identified by 'adult_login';

grant select on adult_login.* to 'adult_login' with grant option;

create table adult_login.users
(
    username varchar(256) primary key,
    password varchar(256)
);

insert into adult_login.users (username, password) values ('admin', 'flag{dummy}');

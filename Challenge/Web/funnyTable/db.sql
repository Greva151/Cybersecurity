create schema funny_table;

create user 'funny_table' identified with mysql_native_password by 'funny_table';

grant select on funny_table.* to 'funny_table' with grant option;

create table funny_table.posts (
    id integer primary key auto_increment,
    title text,
    content text
);

insert into funny_table.posts (title, content) values ('SQLi', 'pls do not do sql injections');
insert into funny_table.posts (title, content) values ('SSRF', 'pls do not do server side request forgery');
insert into funny_table.posts (title, content) values ('Command Injection', 'pls do not do command injections');
insert into funny_table.posts (title, content) values ('Code Injections', 'pls do not do code injections');

create table funny_table.flag
(
    f text,
    a text,
    k text,
    e text
);


drop table if exists Pictures;
create table Pictures (
    id integer primary key autoincrement,
    filename text not null,
    filetype text not null,
    visitors text default '[]',
    unique(filename)
);

drop table if exists Users;
create table Users (
    id integer primary key autoincrement,
    username text not null,
    email text not null,
    password text not null,
    registered_on text not null,
    ip text not null,
    unique(username)
)

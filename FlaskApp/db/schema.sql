-- drop table if exists comments;

create table comments (
    id integer primary key autoincrement,
    name text not null,
    content text not null,
    date text not null 
);

create table entries (
      id integer primary key autoincrement,
      content text not null,
      time text not null,
      res text not null
);


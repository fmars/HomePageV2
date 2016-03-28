-- drop table if exists comments;

create table if not exists comments(
    id integer primary key autoincrement,
    name text not null,
    content text not null,
    date text not null 
);
create table if not exists xtodo (
      id integer primary key autoincrement,
      user text not null,
      todo text not null,
      detail text,
      res text not null,
      date text not null
);


#!/bin/sh

rm users.db
rm groups.db
rm boards.db

db="users.db"

sqlite3 $db << END
CREATE TABLE users (
   id  integer primary key autoincrement,
   name varchar(32) NOT NULL UNIQUE,
   password varchar(32) 
);

insert into users(name, password) values('yukito','password');
END

db="groups.db"

sqlite3 $db << END
CREATE TABLE groups (
   username varchar(32) NOT NULL,
   groupname varchar(32) NOT NULL
);

insert into groups values('yukito','test1');
insert into groups values('yukito','test2');
insert into groups values('yukito','test3');
END

db="boards.db"

sqlite3 $db << END
CREATE TABLE test1 (
   boardname varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP
);
END

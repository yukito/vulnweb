#!/bin/sh
# Please execute this script under db directory
# Ex. $ cd db; ./initialize/initdb.sh

rm users.db
rm groups.db
rm groupMembers.db
rm topics.db

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
   id  integer primary key autoincrement,
   groupname varchar(32) NOT NULL UNIQUE,
   description text
);

insert into groups(groupname, description) values('test1','testgroup1');
insert into groups(groupname, description) values('test2','testgroup2');
insert into groups(groupname, description) values('test3','testgroup3');
END

db="groupMembers.db"

sqlite3 $db << END
CREATE TABLE groupMembers (
   username varchar(32) NOT NULL,
   groupname varchar(32) NOT NULL
);

insert into groupMembers values('yukito','test1');
insert into groupMembers values('yukito','test2');
insert into groupMembers values('yukito','test3');
END

db="topics.db"

sqlite3 $db << END
CREATE TABLE test1 (
   id  integer primary key autoincrement,
   topic varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP
);
CREATE TABLE test2 (
   id  integer primary key autoincrement,
   topic varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP
);
CREATE TABLE test3 (
   id  integer primary key autoincrement,
   topic varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP
);

insert into test1(topic, username, details) values('hello1','yukito', 'hello world!!');
insert into test1(topic, username, details) values('hello2','yukito', 'hello world!!');
insert into test1(topic, username, details) values('hello2','yukito', 'hello world!!');
END

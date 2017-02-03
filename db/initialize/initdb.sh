#!/bin/sh
# Please execute this script under db directory
# Ex. $ cd db; ./initialize/initdb.sh

rm vulnweb.db
rm topics.db

db="vulnweb.db"

sqlite3 $db << END
CREATE TABLE users (
   id  integer primary key autoincrement,
   name varchar(32) NOT NULL UNIQUE,
   password varchar(32) ,
   job varchar(32),
   firm varchar(32),
   department varchar(32),
   image blob
);

insert into users(name, password) values('yukito','password');
END

sqlite3 $db << END
CREATE TABLE groups (
   id  integer primary key autoincrement,
   groupname varchar(32) NOT NULL UNIQUE,
   description text,
   image blob
);

insert into groups(groupname, description) values('test1','testgroup1');
insert into groups(groupname, description) values('test2','testgroup2');
insert into groups(groupname, description) values('test3','testgroup3');
END

sqlite3 $db << END
CREATE TABLE groupMembers (
   username varchar(32) NOT NULL,
   groupname varchar(32) NOT NULL,
   role integer default 0
);

insert into groupMembers values('yukito','test1', 1);
insert into groupMembers(username, groupname) values('yukito','test2');
insert into groupMembers(username, groupname) values('yukito','test3');
END

sqlite3 $db << END
CREATE TABLE groupTopics (
   topic varchar(32) NOT NULL,
   groupname varchar(32) NOT NULL
);

insert into groupTopics values('hello1', 'test1');
insert into groupTopics values('hello2', 'test1');
END

sqlite3 $db << END
CREATE TABLE notifications (
   id  integer primary key autoincrement,
   name varchar(32) NOT NULL,
   type varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP
);
END

db="topics.db"

sqlite3 $db << END
CREATE TABLE test1 (
   id  integer primary key autoincrement,
   topic varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP,
   groupname varchar(32) default 'test1'
);
CREATE TABLE test2 (
   id  integer primary key autoincrement,
   topic varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP,
   groupname varchar(32) default 'test2'
);
CREATE TABLE test3 (
   id  integer primary key autoincrement,
   topic varchar(32) NOT NULL,
   username varchar(32) NOT NULL,
   details text,
   timestamp default CURRENT_TIMESTAMP,
   groupname varchar(32) default 'test3'
);

insert into test1(topic, username, details) values('hello1', 'yukito', 'hello world!!');
insert into test1(topic, username, details) values('hello2', 'yukito', 'hello world!!');
insert into test1(topic, username, details) values('hello2', 'yukito', 'hello world!!');
END


drop table if exists rooms cascade;
drop table if exists threads cascade;
drop table if exists messages cascade;

create table rooms (
	id serial primary key,
	title text,
	url text,
	description text,
	created timestamp default now()
);


create table threads (
	id serial primary key,
	room_id integer references rooms,
	question text,
	resolved boolean DEFAULT false,
	date_started timestamp default now()
);

create table messages (
	id bigserial primary key,
	thread_id integer references threads,
	author text,
	content text,
	date_sent timestamp default now()
);


alter table rooms
	add column thread_id integer references threads;
	
	
--- dummy data...
insert into rooms (title, url, description) values ('web.py', 'webpy', 'a place to discuss anything and everything about web.py');
insert into rooms (title, url, description) values ('python', 'python', 'this app is written in it. you know what to do.');
insert into rooms (title, url, description) values ('prototype', 'prototype', 'Prototype is a JavaScript Framework that aims to ease development of dynamic web applications.');
insert into rooms (title, url, description) values ('postgresql', 'postgresql', 'got any questions regarding the popular postgresql database? this is the place to ask.');
    
insert into threads (room_id, question) values (1, 'system::lobby');
insert into threads (room_id, question) values (2, 'system::lobby');
insert into threads (room_id, question) values (3, 'system::lobby');
insert into threads (room_id, question) values (4, 'system::lobby');
    
update rooms set thread_id = 1 where id = 1;
update rooms set thread_id = 2 where id = 2;
update rooms set thread_id = 3 where id = 3;
update rooms set thread_id = 4 where id = 4;
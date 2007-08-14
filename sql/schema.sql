drop table if exists rooms cascade;
drop table if exists threads cascade;
drop table if exists messages cascade;
drop table if exists people cascade;

create table people (
    id serial primary key,
    email text unique,
    name text,
    password text,
    dashboard_messages text,
    clearance int default 1,
    date_joined timestamp default now()
);

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
	summary text not null,
	resolved boolean DEFAULT false,
	date_started timestamp default now()
);

create table messages (
	id bigserial primary key,
	thread_id integer references threads,
	author_id integer references people,
	content text,
	date_sent timestamp default now()
);

alter table rooms
	add column thread_id integer references threads;
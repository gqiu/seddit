drop table if exists rooms cascade;
drop table if exists threads cascade;
drop table if exists messages cascade;
drop table if exists people cascade;
drop table if exists messages cascade;
drop table if exists recent;

create table people (
    id serial primary key,
    email text unique,
    name text,
    password text,
    dashboard_messages text,
    recent_threads text, -- TODO decouple this.
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
	
create table recent (
    id bigserial primary key,
    date_accessed timestamp default now(),
    message text,
    thread_id int references threads
);

create table user_messages (
    id serial primary key,
    message text,
    author_id int references people,
    read boolean default false,
    date_sent timestamp default now()
);

create table thread_archives (
    id serial primary key,
    thread_id int references threads,
    content text,
    date_archived timestamp default now()
);

create table archive_comments (
    id serial primary key,
    thread_id int references threads,
    author_id int references people,
    date_created timestamp default now(),
    message text
);

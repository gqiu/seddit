insert into rooms (title, url, description) values ('web.py', 'webpy', 'a place to discuss anything and everything about web.py');
insert into rooms (title, url, description) values ('python', 'python', 'this app is written in it. you know what to do.');
insert into rooms (title, url, description) values ('prototype', 'prototype', 'Prototype is a JavaScript Framework that aims to ease development of dynamic web applications.');
insert into rooms (title, url, description) values ('postgresql', 'postgresql', 'got any questions regarding the popular postgresql database? this is the place to ask.');
    
insert into threads (room_id, summary, question) values (1, 'system::lobby', 'system::lobby');
insert into threads (room_id, summary, question) values (2, 'system::lobby', 'system::lobby');
insert into threads (room_id, summary, question) values (3, 'system::lobby', 'system::lobby');
insert into threads (room_id, summary, question) values (4, 'system::lobby', 'system::lobby');
    
update rooms set thread_id = 1 where id = 1;
update rooms set thread_id = 2 where id = 2;
update rooms set thread_id = 3 where id = 3;
update rooms set thread_id = 4 where id = 4;

insert into people (email, name) values ('system@seddit.local', 'system');
insert into people (email, name) values ('drew@revision1.net', 'drew');
insert into people (email, name) values ('billy joe', 'billy@joe.com');

insert into people(email, name) values('guest@seddit.local', 'guest');
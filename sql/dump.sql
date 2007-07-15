-- Table: messages
DROP TABLE messages;
CREATE TABLE messages
(
  id bigserial NOT NULL,
  thread_id integer,
  author text,
  content text,
  date_sent timestamp with time zone DEFAULT now(),
  CONSTRAINT messages_pkey PRIMARY KEY (id),
  CONSTRAINT messages_thread_id_fkey FOREIGN KEY (thread_id)
      REFERENCES threads (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)

-- Table: rooms
DROP TABLE rooms;
CREATE TABLE rooms
(
  id serial NOT NULL,
  title text,
  description text,
  created timestamp without time zone DEFAULT timezone('utc'::text, now()),
  url text,
  thread_id integer,
  CONSTRAINT rooms_pkey PRIMARY KEY (id),
  CONSTRAINT rooms_thread_id_fkey FOREIGN KEY (thread_id)
      REFERENCES threads (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)


-- Table: threads
DROP TABLE threads;
CREATE TABLE threads
(
  id serial NOT NULL,
  room_id integer,
  question text,
  resolved boolean DEFAULT false,
  date_started timestamp without time zone DEFAULT timezone('utc'::text, now()),
  CONSTRAINT threads_pkey PRIMARY KEY (id),
  CONSTRAINT threads_room_id_fkey FOREIGN KEY (room_id)
      REFERENCES rooms (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)



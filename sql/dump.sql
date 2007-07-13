--
-- PostgreSQL database dump
--

SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: dnewberry
--

COMMENT ON SCHEMA public IS 'Standard public schema';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: dnewberry; Tablespace: 
--

CREATE TABLE messages (
    id bigint NOT NULL,
    thread_id integer,
    author text,
    content text,
    date_sent timestamp with time zone DEFAULT now()
);


ALTER TABLE public.messages OWNER TO dnewberry;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: dnewberry
--

CREATE SEQUENCE messages_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.messages_id_seq OWNER TO dnewberry;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnewberry
--

ALTER SEQUENCE messages_id_seq OWNED BY messages.id;


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnewberry
--

SELECT pg_catalog.setval('messages_id_seq', 9, true);


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: dnewberry; Tablespace: 
--

CREATE TABLE rooms (
    id integer NOT NULL,
    title text,
    description text,
    created timestamp without time zone DEFAULT timezone('utc'::text, now()),
    url text,
    thread_id integer
);


ALTER TABLE public.rooms OWNER TO dnewberry;

--
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: dnewberry
--

CREATE SEQUENCE rooms_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.rooms_id_seq OWNER TO dnewberry;

--
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnewberry
--

ALTER SEQUENCE rooms_id_seq OWNED BY rooms.id;


--
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnewberry
--

SELECT pg_catalog.setval('rooms_id_seq', 1, true);


--
-- Name: threads; Type: TABLE; Schema: public; Owner: dnewberry; Tablespace: 
--

CREATE TABLE threads (
    id integer NOT NULL,
    room_id integer,
    question text,
    resolved boolean DEFAULT false,
    date_started timestamp without time zone DEFAULT timezone('utc'::text, now())
);


ALTER TABLE public.threads OWNER TO dnewberry;

--
-- Name: threads_id_seq; Type: SEQUENCE; Schema: public; Owner: dnewberry
--

CREATE SEQUENCE threads_id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.threads_id_seq OWNER TO dnewberry;

--
-- Name: threads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dnewberry
--

ALTER SEQUENCE threads_id_seq OWNED BY threads.id;


--
-- Name: threads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dnewberry
--

SELECT pg_catalog.setval('threads_id_seq', 1, true);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dnewberry
--

ALTER TABLE messages ALTER COLUMN id SET DEFAULT nextval('messages_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dnewberry
--

ALTER TABLE rooms ALTER COLUMN id SET DEFAULT nextval('rooms_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dnewberry
--

ALTER TABLE threads ALTER COLUMN id SET DEFAULT nextval('threads_id_seq'::regclass);


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: dnewberry
--

COPY messages (id, thread_id, author, content, date_sent) FROM stdin;
1	1	drew	this is cool	2007-07-11 16:41:49.12099-07
2	1	harry	ya, it is	2007-07-11 16:42:05.371591-07
3	1	drew	hi there	2007-07-12 12:19:15.214922-07
4	1	drew	hi there	2007-07-12 12:19:15.969128-07
5	1	drew	hi there	2007-07-12 12:19:16.504099-07
6	1	drew	hi there	2007-07-12 12:19:16.942601-07
7	1	drew	hi there	2007-07-12 12:19:17.552376-07
8	1	drew	hi there	2007-07-12 12:19:18.105257-07
9	1	drew	hi there	2007-07-12 12:19:40.90547-07
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: dnewberry
--

COPY rooms (id, title, description, created, url, thread_id) FROM stdin;
1	web.py	a place to discuss anything and everything about web.py	2007-07-11 23:39:37.6377	webpy	\N
\.


--
-- Data for Name: threads; Type: TABLE DATA; Schema: public; Owner: dnewberry
--

COPY threads (id, room_id, question, resolved, date_started) FROM stdin;
1	1	how do i start a web.py dev server?	f	2007-07-11 23:40:59.082676
\.


--
-- Name: messages_pkey; Type: CONSTRAINT; Schema: public; Owner: dnewberry; Tablespace: 
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: dnewberry; Tablespace: 
--

ALTER TABLE ONLY rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- Name: threads_pkey; Type: CONSTRAINT; Schema: public; Owner: dnewberry; Tablespace: 
--

ALTER TABLE ONLY threads
    ADD CONSTRAINT threads_pkey PRIMARY KEY (id);


--
-- Name: messages_thread_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dnewberry
--

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_thread_id_fkey FOREIGN KEY (thread_id) REFERENCES threads(id);


--
-- Name: rooms_thread_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dnewberry
--

ALTER TABLE ONLY rooms
    ADD CONSTRAINT rooms_thread_id_fkey FOREIGN KEY (thread_id) REFERENCES threads(id);


--
-- Name: threads_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dnewberry
--

ALTER TABLE ONLY threads
    ADD CONSTRAINT threads_room_id_fkey FOREIGN KEY (room_id) REFERENCES rooms(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: dnewberry
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM dnewberry;
GRANT ALL ON SCHEMA public TO dnewberry;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--

\restrict CANjmneRsZMYQ01vHZKfu1jUqHwOh4hjqirm3nlU99qNqWMDwzvDRA37MwispXK

-- Dumped from database version 15.18 (Debian 15.18-1.pgdg13+1)
-- Dumped by pg_dump version 15.18 (Debian 15.18-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    task_type text NOT NULL,
    payload jsonb NOT NULL,
    priority integer DEFAULT 100,
    status text DEFAULT 'pending'::text,
    attempts integer DEFAULT 0,
    max_attempts integer DEFAULT 3,
    locked_at timestamp without time zone,
    lease_until timestamp without time zone,
    worker_id text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    started_at timestamp without time zone,
    finished_at timestamp without time zone,
    error_message text
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_id_seq OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, task_type, payload, priority, status, attempts, max_attempts, locked_at, lease_until, worker_id, created_at, updated_at, started_at, finished_at, error_message) FROM stdin;
1	route_search	{"origin": "MOW", "destination": "IST"}	100	done	0	3	2026-06-09 05:57:56.965942	2026-06-09 06:07:56.965942	worker	2026-06-09 05:57:54.959865	2026-06-09 05:57:56.977154	\N	2026-06-09 05:57:56.977154	\N
\.


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 1, true);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: idx_tasks_status_priority; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tasks_status_priority ON public.tasks USING btree (status, priority DESC, id);


--
-- PostgreSQL database dump complete
--

\unrestrict CANjmneRsZMYQ01vHZKfu1jUqHwOh4hjqirm3nlU99qNqWMDwzvDRA37MwispXK


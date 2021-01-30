--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1 (Debian 13.1-1.pgdg100+1)
-- Dumped by pg_dump version 13.1 (Debian 13.1-1.pgdg100+1)

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
-- Name: fees; Type: TABLE; Schema: public; Owner: zapata
--

CREATE TABLE public.fees (
    id integer NOT NULL,
    yearly integer
);


ALTER TABLE public.fees OWNER TO zapata;

--
-- Name: fees_id_seq; Type: SEQUENCE; Schema: public; Owner: zapata
--

CREATE SEQUENCE public.fees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fees_id_seq OWNER TO zapata;

--
-- Name: fees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zapata
--

ALTER SEQUENCE public.fees_id_seq OWNED BY public.fees.id;


--
-- Name: incidents; Type: TABLE; Schema: public; Owner: zapata
--

CREATE TABLE public.incidents (
    id integer NOT NULL,
    description character varying
);


ALTER TABLE public.incidents OWNER TO zapata;

--
-- Name: incidents_id_seq; Type: SEQUENCE; Schema: public; Owner: zapata
--

CREATE SEQUENCE public.incidents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.incidents_id_seq OWNER TO zapata;

--
-- Name: incidents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zapata
--

ALTER SEQUENCE public.incidents_id_seq OWNED BY public.incidents.id;


--
-- Name: income; Type: TABLE; Schema: public; Owner: zapata
--

CREATE TABLE public.income (
    index bigint,
    "Total" bigint,
    "Jan" bigint,
    "Feb" bigint,
    "Monthly" bigint,
    "Balance" bigint,
    "Alert" boolean
);


ALTER TABLE public.income OWNER TO zapata;

--
-- Name: fees id; Type: DEFAULT; Schema: public; Owner: zapata
--

ALTER TABLE ONLY public.fees ALTER COLUMN id SET DEFAULT nextval('public.fees_id_seq'::regclass);


--
-- Name: incidents id; Type: DEFAULT; Schema: public; Owner: zapata
--

ALTER TABLE ONLY public.incidents ALTER COLUMN id SET DEFAULT nextval('public.incidents_id_seq'::regclass);


--
-- Data for Name: fees; Type: TABLE DATA; Schema: public; Owner: zapata
--

COPY public.fees (id, yearly) FROM stdin;
\.


--
-- Data for Name: incidents; Type: TABLE DATA; Schema: public; Owner: zapata
--

COPY public.incidents (id, description) FROM stdin;
1	חיפויים
2	נזילת מים בחדר דוודים קומה 3
3	תאורת לובי קומות 3-4
4	להוציא קבלה ליפה כדורי על סך 700 ש״ח
5	לשלם לליאורה מילבאום 37.5 ש״ח בגין רכישת קבלות
6	תשלום לגנן הקודם - 1200 ש״ח
7	שכפול מפתחות לחדר אופניים
8	אינטרקום - הורדת עוצמת הצלצול
\.


--
-- Data for Name: income; Type: TABLE DATA; Schema: public; Owner: zapata
--

COPY public.income (index, "Total", "Jan", "Feb", "Monthly", "Balance", "Alert") FROM stdin;
1	5400	1350	0	450	4050	f
2	5400	450	0	450	4950	f
3	3780	3780	0	315	0	f
4	3780	315	0	315	3465	f
5	3780	945	0	315	2835	f
6	3780	630	0	315	3150	f
7	3780	315	0	315	3465	f
8	4500	2250	0	375	2250	f
9	4500	1125	0	375	3375	f
10	4860	1215	0	405	3645	f
11	5400	450	0	450	4950	f
12	5400	1350	0	450	4050	f
13	4860	810	0	405	4050	f
14	5400	5400	0	450	0	f
15	4860	1215	0	405	3645	f
16	5400	1350	0	450	4050	f
17	4860	405	0	405	4455	f
18	7200	3600	0	600	3600	f
19	7200	600	0	600	6600	f
\.


--
-- Name: fees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zapata
--

SELECT pg_catalog.setval('public.fees_id_seq', 1, false);


--
-- Name: incidents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zapata
--

SELECT pg_catalog.setval('public.incidents_id_seq', 8, true);


--
-- Name: fees fees_pkey; Type: CONSTRAINT; Schema: public; Owner: zapata
--

ALTER TABLE ONLY public.fees
    ADD CONSTRAINT fees_pkey PRIMARY KEY (id);


--
-- Name: incidents incidents_pkey; Type: CONSTRAINT; Schema: public; Owner: zapata
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT incidents_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

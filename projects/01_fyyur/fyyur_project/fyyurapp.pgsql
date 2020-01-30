--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5
-- Dumped by pg_dump version 11.5

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

SET default_with_oids = false;

--
-- Name: Artist; Type: TABLE; Schema: public; Owner: syedahmedhussain
--

CREATE TABLE public."Artist" (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    phone character varying(120),
    genres character varying[],
    website character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    seeking_venue boolean,
    seeking_description character varying(500)
);


ALTER TABLE public."Artist" OWNER TO syedahmedhussain;

--
-- Name: Artist_id_seq; Type: SEQUENCE; Schema: public; Owner: syedahmedhussain
--

CREATE SEQUENCE public."Artist_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Artist_id_seq" OWNER TO syedahmedhussain;

--
-- Name: Artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: syedahmedhussain
--

ALTER SEQUENCE public."Artist_id_seq" OWNED BY public."Artist".id;


--
-- Name: Show; Type: TABLE; Schema: public; Owner: syedahmedhussain
--

CREATE TABLE public."Show" (
    id integer NOT NULL,
    venue_id integer NOT NULL,
    artist_id integer NOT NULL,
    start_time character varying NOT NULL
);


ALTER TABLE public."Show" OWNER TO syedahmedhussain;

--
-- Name: Show_id_seq; Type: SEQUENCE; Schema: public; Owner: syedahmedhussain
--

CREATE SEQUENCE public."Show_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Show_id_seq" OWNER TO syedahmedhussain;

--
-- Name: Show_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: syedahmedhussain
--

ALTER SEQUENCE public."Show_id_seq" OWNED BY public."Show".id;


--
-- Name: Venue; Type: TABLE; Schema: public; Owner: syedahmedhussain
--

CREATE TABLE public."Venue" (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    address character varying(120),
    phone character varying(120),
    genres character varying[],
    website character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    seeking_talent boolean,
    seeking_description character varying(500)
);


ALTER TABLE public."Venue" OWNER TO syedahmedhussain;

--
-- Name: Venue_id_seq; Type: SEQUENCE; Schema: public; Owner: syedahmedhussain
--

CREATE SEQUENCE public."Venue_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Venue_id_seq" OWNER TO syedahmedhussain;

--
-- Name: Venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: syedahmedhussain
--

ALTER SEQUENCE public."Venue_id_seq" OWNED BY public."Venue".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: syedahmedhussain
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO syedahmedhussain;

--
-- Name: Artist id; Type: DEFAULT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Artist" ALTER COLUMN id SET DEFAULT nextval('public."Artist_id_seq"'::regclass);


--
-- Name: Show id; Type: DEFAULT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Show" ALTER COLUMN id SET DEFAULT nextval('public."Show_id_seq"'::regclass);


--
-- Name: Venue id; Type: DEFAULT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Venue" ALTER COLUMN id SET DEFAULT nextval('public."Venue_id_seq"'::regclass);


--
-- Data for Name: Artist; Type: TABLE DATA; Schema: public; Owner: syedahmedhussain
--

COPY public."Artist" (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description) FROM stdin;
1	tester2	testers City	AL	123542134	{Classical,Country,Electronic,Folk}	\N	\N		\N	\N
2	Guns N Petals	San Francisco	CA	3261235000	{Alternative,Blues,Classical}	\N	\N		\N	\N
3	The Wild Sax Band	San Francisco	CA	4323255432	{Alternative,Classical}	\N	\N		\N	\N
4	Matt Quevedo	New York	NY	3004005000	{Classical,Country}	\N	\N		\N	\N
\.


--
-- Data for Name: Show; Type: TABLE DATA; Schema: public; Owner: syedahmedhussain
--

COPY public."Show" (id, venue_id, artist_id, start_time) FROM stdin;
1	2	1	2020-12-18 10:36:20
\.


--
-- Data for Name: Venue; Type: TABLE DATA; Schema: public; Owner: syedahmedhussain
--

COPY public."Venue" (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) FROM stdin;
1	Texas North Rodeo Hall	amarillo	TX	4133 Pacific dr, greenbarn	4132234576	{Alternative,Blues,Country}	\N	\N		\N	\N
2	News Texas Hall	Mckinney	TX	asdsa 3e safa	sa;21321	{Blues,Classical,Country}	\N	\N		\N	\N
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: syedahmedhussain
--

COPY public.alembic_version (version_num) FROM stdin;
cd6649b93e65
\.


--
-- Name: Artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: syedahmedhussain
--

SELECT pg_catalog.setval('public."Artist_id_seq"', 4, true);


--
-- Name: Show_id_seq; Type: SEQUENCE SET; Schema: public; Owner: syedahmedhussain
--

SELECT pg_catalog.setval('public."Show_id_seq"', 1, true);


--
-- Name: Venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: syedahmedhussain
--

SELECT pg_catalog.setval('public."Venue_id_seq"', 2, true);


--
-- Name: Artist Artist_pkey; Type: CONSTRAINT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Artist"
    ADD CONSTRAINT "Artist_pkey" PRIMARY KEY (id);


--
-- Name: Show Show_pkey; Type: CONSTRAINT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Show"
    ADD CONSTRAINT "Show_pkey" PRIMARY KEY (id);


--
-- Name: Venue Venue_pkey; Type: CONSTRAINT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Venue"
    ADD CONSTRAINT "Venue_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: Show Show_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Show"
    ADD CONSTRAINT "Show_artist_id_fkey" FOREIGN KEY (artist_id) REFERENCES public."Artist"(id);


--
-- Name: Show Show_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: syedahmedhussain
--

ALTER TABLE ONLY public."Show"
    ADD CONSTRAINT "Show_venue_id_fkey" FOREIGN KEY (venue_id) REFERENCES public."Venue"(id);


--
-- PostgreSQL database dump complete
--


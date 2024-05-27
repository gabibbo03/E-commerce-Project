--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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

--
-- Name: Ecommerce; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "Ecommerce" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Italian_Italy.1252';


ALTER DATABASE "Ecommerce" OWNER TO postgres;

\connect "Ecommerce"

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

--
-- Name: DATABASE "Ecommerce"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE "Ecommerce" IS 'DataBase fatta in postgres';


--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Carrello; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Carrello" (
    "Id_carrello_entry" bigint DEFAULT 1 NOT NULL,
    qta bigint DEFAULT 0 NOT NULL
);


ALTER TABLE public."Carrello" OWNER TO postgres;

--
-- Name: TABLE "Carrello"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Carrello" IS 'tabella Carrelli : Esiste una tabella carrello globale in cui  in ogni entry viene salvata quale prodotto un utente vuole comprare : user | Id_prodotto.
';


--
-- Name: CarrelloUtenti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."CarrelloUtenti" (
    id_carrello_entry bigint,
    "user" "char"[] NOT NULL,
    "Pk_CarrelloUtenti" bigint DEFAULT 1 NOT NULL
);


ALTER TABLE public."CarrelloUtenti" OWNER TO postgres;

--
-- Name: Prodotti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Prodotti" (
    id_prodotto bigint NOT NULL,
    "Titolo" "char"[] NOT NULL,
    "Descrizione" "char"[] NOT NULL,
    data_pubblicazione date NOT NULL,
    nuovo boolean DEFAULT true NOT NULL,
    "Prezzo" double precision DEFAULT 0.0 NOT NULL
);


ALTER TABLE public."Prodotti" OWNER TO postgres;

--
-- Name: TABLE "Prodotti"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Prodotti" IS 'Schema Prodotti';


--
-- Name: ProdottiCarrelli; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ProdottiCarrelli" (
    id_prodotto bigint,
    id_carrello_entry bigint,
    "PK_ProdottiCarrelli" bigint NOT NULL
);


ALTER TABLE public."ProdottiCarrelli" OWNER TO postgres;

--
-- Name: TABLE "ProdottiCarrelli"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."ProdottiCarrelli" IS 'Tabella che assoccia ogni prodotto presente nella tabella Prodotti a quale carrello appartiene
(cerchiamo quindi di associare ogni prodotto un Id_carrello il quale è associato un utente)';


--
-- Name: ProdottiRecensioni; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ProdottiRecensioni" (
    id_recensione_entry bigint,
    id_prodotto bigint,
    "PK_ProdottiRecensioni" bigint NOT NULL
);


ALTER TABLE public."ProdottiRecensioni" OWNER TO postgres;

--
-- Name: TABLE "ProdottiRecensioni"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."ProdottiRecensioni" IS 'Tabella che assoccia ad un prodotto una recensione';


--
-- Name: ProdottiStorici; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ProdottiStorici" (
    id_prodotto bigint,
    id_storico_entry bigint,
    "PK_ProdottiStorici" bigint NOT NULL
);


ALTER TABLE public."ProdottiStorici" OWNER TO postgres;

--
-- Name: ProdottiTag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ProdottiTag" (
    "Termine" "char"[],
    id_prodotto bigint,
    "PK_ProdottiTag" bigint NOT NULL
);


ALTER TABLE public."ProdottiTag" OWNER TO postgres;

--
-- Name: TABLE "ProdottiTag"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."ProdottiTag" IS 'tabella che assoccia ad ogni prodotto un tag';


--
-- Name: ProdottiUtenti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ProdottiUtenti" (
    "user" "char"[],
    id_prodotto bigint,
    "PK_ProdottiUtenti" bigint NOT NULL
);


ALTER TABLE public."ProdottiUtenti" OWNER TO postgres;

--
-- Name: TABLE "ProdottiUtenti"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."ProdottiUtenti" IS 'Ogni Utente può mettere un annuncio per vendere più prodotti';


--
-- Name: Recensioni; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Recensioni" (
    numero_stelle bigint DEFAULT 0 NOT NULL,
    titolo "char"[] NOT NULL,
    descrizione "char"[],
    "Id_recensione_entry" bigint NOT NULL,
    "Data" date NOT NULL
);


ALTER TABLE public."Recensioni" OWNER TO postgres;

--
-- Name: TABLE "Recensioni"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Recensioni" IS 'tabella Recensioni';


--
-- Name: Storico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Storico" (
    "Data" date NOT NULL,
    "Nome" "char"[] NOT NULL,
    id_storico_entry bigint NOT NULL
);


ALTER TABLE public."Storico" OWNER TO postgres;

--
-- Name: TABLE "Storico"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Storico" IS 'Tabella storici base';


--
-- Name: Tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Tag" (
    "Termine" "char"[] NOT NULL
);


ALTER TABLE public."Tag" OWNER TO postgres;

--
-- Name: TABLE "Tag"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Tag" IS 'Lista delle possibili parole salvate e usate per la barra di ricerca';


--
-- Name: Utenti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Utenti" (
    media_recensioni_ricevute double precision DEFAULT 0.0,
    "user" character varying(256) NOT NULL,
    password bytea,
    contatto_mail character varying(256) NOT NULL,
    contatto_tel character varying(11)
);


ALTER TABLE public."Utenti" OWNER TO postgres;

--
-- Name: TABLE "Utenti"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Utenti" IS 'Schema Utenti 
';


--
-- Data for Name: Carrello; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Carrello" ("Id_carrello_entry", qta) FROM stdin;
\.


--
-- Data for Name: CarrelloUtenti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."CarrelloUtenti" (id_carrello_entry, "user", "Pk_CarrelloUtenti") FROM stdin;
\.


--
-- Data for Name: Prodotti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Prodotti" (id_prodotto, "Titolo", "Descrizione", data_pubblicazione, nuovo, "Prezzo") FROM stdin;
\.


--
-- Data for Name: ProdottiCarrelli; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ProdottiCarrelli" (id_prodotto, id_carrello_entry, "PK_ProdottiCarrelli") FROM stdin;
\.


--
-- Data for Name: ProdottiRecensioni; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ProdottiRecensioni" (id_recensione_entry, id_prodotto, "PK_ProdottiRecensioni") FROM stdin;
\.


--
-- Data for Name: ProdottiStorici; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ProdottiStorici" (id_prodotto, id_storico_entry, "PK_ProdottiStorici") FROM stdin;
\.


--
-- Data for Name: ProdottiTag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ProdottiTag" ("Termine", id_prodotto, "PK_ProdottiTag") FROM stdin;
\.


--
-- Data for Name: ProdottiUtenti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ProdottiUtenti" ("user", id_prodotto, "PK_ProdottiUtenti") FROM stdin;
\.


--
-- Data for Name: Recensioni; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Recensioni" (numero_stelle, titolo, descrizione, "Id_recensione_entry", "Data") FROM stdin;
\.


--
-- Data for Name: Storico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Storico" ("Data", "Nome", id_storico_entry) FROM stdin;
\.


--
-- Data for Name: Tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Tag" ("Termine") FROM stdin;
\.


--
-- Data for Name: Utenti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Utenti" (media_recensioni_ricevute, "user", password, contatto_mail, contatto_tel) FROM stdin;
0	gabriele	\\x3e15345b486895a320ee5eaa02f8038aeb578fd280edaca701ed15d82333723802df5491d3bafbbbd6cb6eabf42125ac	gabrycus03@gmail.com	\N
0	agnese	\\x5c8809a85e295aa280b93a9e318a5fbb6244846adfdc8f6f9ebda7934648d33fa772ec955b41feeb1de1764bd59cb7cd	agnyflute02@gmail.com	\N
0	giancarlo	\\xcc84a3495b811f8ebc0a97f6d222fe4cfcfc68575707c68f58cce757d85b2bab341fe78074bf5b452a7a0072bf628775	giancus1@alice.it	\N
0	adriana	\\x9ba56b9d75eebc7ab41c97e3a32da95c6f1341b30f3763941c2b36dc011474b3420f5fc521235ce53648fee67f8ba3ed	adrianacaruso@gmail.com	\N
0	francesco	\\x655ab4ea6b802e340828cd25498d0a2aa201dc023e4b3bfff5809592bd6fa72ab3be91e6108deb0acb30494e95231af1	francycusano@gmail.com	\N
\.


--
-- Name: CarrelloUtenti PK_CarrelloUtenti; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CarrelloUtenti"
    ADD CONSTRAINT "PK_CarrelloUtenti" PRIMARY KEY ("Pk_CarrelloUtenti");


--
-- Name: ProdottiCarrelli PK_ProdottiCarrelli; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiCarrelli"
    ADD CONSTRAINT "PK_ProdottiCarrelli" PRIMARY KEY ("PK_ProdottiCarrelli");


--
-- Name: ProdottiRecensioni PK_ProdottiRecensioni; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiRecensioni"
    ADD CONSTRAINT "PK_ProdottiRecensioni" PRIMARY KEY ("PK_ProdottiRecensioni");


--
-- Name: ProdottiStorici PK_ProdottiStorici; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiStorici"
    ADD CONSTRAINT "PK_ProdottiStorici" PRIMARY KEY ("PK_ProdottiStorici");


--
-- Name: ProdottiTag PK_ProdottiTag; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiTag"
    ADD CONSTRAINT "PK_ProdottiTag" PRIMARY KEY ("PK_ProdottiTag");


--
-- Name: ProdottiUtenti PK_ProdottiUtenti; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiUtenti"
    ADD CONSTRAINT "PK_ProdottiUtenti" PRIMARY KEY ("PK_ProdottiUtenti");


--
-- Name: Prodotti Prodotti_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Prodotti"
    ADD CONSTRAINT "Prodotti_pkey" PRIMARY KEY (id_prodotto);


--
-- Name: Recensioni Recensioni_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Recensioni"
    ADD CONSTRAINT "Recensioni_pkey" PRIMARY KEY ("Id_recensione_entry");


--
-- Name: Carrello id_carrello_entry; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Carrello"
    ADD CONSTRAINT id_carrello_entry PRIMARY KEY ("Id_carrello_entry") INCLUDE ("Id_carrello_entry");


--
-- Name: Storico id_storico_entry; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Storico"
    ADD CONSTRAINT id_storico_entry PRIMARY KEY (id_storico_entry) INCLUDE (id_storico_entry);


--
-- Name: Utenti pk_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Utenti"
    ADD CONSTRAINT pk_user PRIMARY KEY ("user");


--
-- Name: Tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Tag"
    ADD CONSTRAINT tag_pkey PRIMARY KEY ("Termine");


--
-- Name: fki_User; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_User" ON public."CarrelloUtenti" USING btree ("user");


--
-- Name: ProdottiTag Termine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiTag"
    ADD CONSTRAINT "Termine" FOREIGN KEY ("Termine") REFERENCES public."Tag"("Termine");


--
-- Name: ProdottiCarrelli id_carrello_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiCarrelli"
    ADD CONSTRAINT id_carrello_entry FOREIGN KEY (id_carrello_entry) REFERENCES public."Carrello"("Id_carrello_entry");


--
-- Name: CarrelloUtenti id_carrello_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CarrelloUtenti"
    ADD CONSTRAINT id_carrello_entry FOREIGN KEY (id_carrello_entry) REFERENCES public."Carrello"("Id_carrello_entry");


--
-- Name: ProdottiCarrelli id_prodotto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiCarrelli"
    ADD CONSTRAINT id_prodotto FOREIGN KEY (id_prodotto) REFERENCES public."Prodotti"(id_prodotto);


--
-- Name: ProdottiUtenti id_prodotto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiUtenti"
    ADD CONSTRAINT id_prodotto FOREIGN KEY (id_prodotto) REFERENCES public."Prodotti"(id_prodotto);


--
-- Name: ProdottiStorici id_prodotto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiStorici"
    ADD CONSTRAINT id_prodotto FOREIGN KEY (id_prodotto) REFERENCES public."Prodotti"(id_prodotto);


--
-- Name: ProdottiRecensioni id_prodotto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiRecensioni"
    ADD CONSTRAINT id_prodotto FOREIGN KEY (id_prodotto) REFERENCES public."Prodotti"(id_prodotto);


--
-- Name: ProdottiTag id_prodotto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiTag"
    ADD CONSTRAINT id_prodotto FOREIGN KEY (id_prodotto) REFERENCES public."Prodotti"(id_prodotto);


--
-- Name: ProdottiRecensioni id_recensioni_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiRecensioni"
    ADD CONSTRAINT id_recensioni_entry FOREIGN KEY (id_recensione_entry) REFERENCES public."Recensioni"("Id_recensione_entry");


--
-- Name: ProdottiStorici id_storico_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiStorici"
    ADD CONSTRAINT id_storico_entry FOREIGN KEY (id_storico_entry) REFERENCES public."Storico"(id_storico_entry);


--
-- PostgreSQL database dump complete
--


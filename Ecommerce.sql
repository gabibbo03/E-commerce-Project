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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Carrello; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Carrello" (
    "Id_carrello_entry" bigint NOT NULL,
    qta bigint DEFAULT 0 NOT NULL
);


ALTER TABLE public."Carrello" OWNER TO postgres;

--
-- Name: TABLE "Carrello"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Carrello" IS 'tabella Carrelli : Esiste una tabella carrello globale in cui  in ogni entry viene salvata quale prodotto un utente vuole comprare : user | Id_prodotto.
';


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
    id_carrello_entry bigint
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
    id_prodotto bigint
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
    id_storico_entry bigint
);


ALTER TABLE public."ProdottiStorici" OWNER TO postgres;

--
-- Name: ProdottiTag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ProdottiTag" (
    "Termine" "char"[],
    id_prodotto bigint
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
    id_prodotto bigint
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
-- Name: Utenti; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Utenti" (
    "user" "char"[] NOT NULL,
    password "char"[] NOT NULL,
    media_recensioni_ricevute double precision DEFAULT 0.0,
    contatto_mail "char"[] NOT NULL,
    contatto_tel "char"[]
);


ALTER TABLE public."Utenti" OWNER TO postgres;

--
-- Name: TABLE "Utenti"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."Utenti" IS 'Schema Utenti 
';


--
-- Name: UtentiCarrelli; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UtentiCarrelli" (
    "user" "char"[] NOT NULL,
    id_carrello_entry bigint NOT NULL
);


ALTER TABLE public."UtentiCarrelli" OWNER TO postgres;

--
-- Name: TABLE "UtentiCarrelli"; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public."UtentiCarrelli" IS 'Tabella che associa ad ogni utente un carrello';


--
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
    "Termine" "char"[] NOT NULL
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- Name: TABLE tag; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tag IS 'Lista delle possibili parole salvate e usate per la barra di ricerca';


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
-- Name: Utenti Utenti_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Utenti"
    ADD CONSTRAINT "Utenti_pkey" PRIMARY KEY ("user");


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
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY ("Termine");


--
-- Name: fki_id_carrello_entry; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_id_carrello_entry ON public."UtentiCarrelli" USING btree (id_carrello_entry);


--
-- Name: ProdottiTag Termine; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiTag"
    ADD CONSTRAINT "Termine" FOREIGN KEY ("Termine") REFERENCES public.tag("Termine");


--
-- Name: UtentiCarrelli id_carrello_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UtentiCarrelli"
    ADD CONSTRAINT id_carrello_entry FOREIGN KEY (id_carrello_entry) REFERENCES public."Carrello"("Id_carrello_entry") NOT VALID;


--
-- Name: ProdottiCarrelli id_carrello_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiCarrelli"
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
-- Name: UtentiCarrelli user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UtentiCarrelli"
    ADD CONSTRAINT "user" FOREIGN KEY ("user") REFERENCES public."Utenti"("user");


--
-- Name: ProdottiUtenti user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ProdottiUtenti"
    ADD CONSTRAINT "user" FOREIGN KEY ("user") REFERENCES public."Utenti"("user");


--
-- PostgreSQL database dump complete
--


-- Skript pro vytvoreni databaze na hromadnou konzultaci Dovoz pizzy
--
--
DROP TABLE Uzivatel CASCADE CONSTRAINTS;
DROP TABLE Vlastnik CASCADE CONSTRAINTS;
DROP TABLE Zakaznik CASCADE CONSTRAINTS;
DROP TABLE Bavic CASCADE CONSTRAINTS;
DROP TABLE Pizzerie CASCADE CONSTRAINTS;
DROP TABLE Pracovnik CASCADE CONSTRAINTS;
DROP TABLE Druh CASCADE CONSTRAINTS;
DROP TABLE Zabava CASCADE CONSTRAINTS;
DROP TABLE Ovlada CASCADE CONSTRAINTS;
DROP TABLE Objednavka CASCADE CONSTRAINTS;
DROP TABLE Obsahuje CASCADE CONSTRAINTS;

CREATE TABLE Uzivatel (
    id_u NUMERIC(7,0) NOT NULL,
    jmeno VARCHAR(30),
    datum_narozeni DATE,
    adresa VARCHAR(50),
    CONSTRAINT PK_uzivatel PRIMARY KEY (id_u)
);

CREATE TABLE Vlastnik (
    id_u NUMERIC(7,0) NOT NULL,
    linkedin VARCHAR(30),
    CONSTRAINT PK_vlastnik PRIMARY KEY (id_u),
    CONSTRAINT FK_vlastnik_idu FOREIGN KEY (id_u) REFERENCES Uzivatel
);

CREATE TABLE Zakaznik (
    id_u NUMERIC(7,0) NOT NULL,
    adresa_doruceni VARCHAR(50) NOT NULL,
    CONSTRAINT PK_zakaznik PRIMARY KEY (id_u),
    CONSTRAINT FK_zakaznik_idu FOREIGN KEY (id_u) REFERENCES Uzivatel
);

CREATE TABLE Bavic (
    id_u NUMERIC(7,0) NOT NULL,
    nazev_sceny VARCHAR(30),
    zivotopis VARCHAR(500),
    cena NUMERIC(4,0) NOT NULL,
    CONSTRAINT PK_bavic PRIMARY KEY (id_u),
    CONSTRAINT FK_bavic_idu FOREIGN KEY (id_u) REFERENCES Uzivatel
);

CREATE TABLE Pizzerie (
    id_p NUMERIC(7,0) NOT NULL,
    nazev VARCHAR(30),
    ulice VARCHAR(30),
    mesto VARCHAR(30),
    psc NUMERIC(5,0),
    telefon NUMERIC(9,0),
    oteviraci_doba VARCHAR(50),
    id_u NUMERIC(7,0) NOT NULL,
    CONSTRAINT PK_pizzerie_idp PRIMARY KEY (id_p),
    CONSTRAINT FK_pizzerie_idu FOREIGN KEY (id_u) REFERENCES Vlastnik
);

CREATE TABLE Pracovnik (
    id_p NUMERIC(7,0) NOT NULL,
    id_u NUMERIC(7,0) NOT NULL,
    dostupnost VARCHAR(50),
    CONSTRAINT PK_pracovnik PRIMARY KEY (id_p,id_u),
    CONSTRAINT FK_pracovnik_idp FOREIGN KEY (id_p) REFERENCES Pizzerie,
    CONSTRAINT FK_pracovnik_idu FOREIGN KEY (id_u) REFERENCES Bavic
);

CREATE TABLE Druh (
    jmeno_p VARCHAR(30) NOT NULL,
    obsah VARCHAR(50),
    cena DECIMAL(4,0),
    id_p NUMERIC(7,0) NOT NULL,
    CONSTRAINT PK_druh_jmenopidp PRIMARY KEY (jmeno_p,id_p),
    CONSTRAINT FK_druh_idp FOREIGN KEY (id_p) REFERENCES Pizzerie
);

CREATE TABLE Zabava (
    druh_zabavy VARCHAR(30),
    CONSTRAINT PK_zabava_nazevzabavy PRIMARY KEY (druh_zabavy)
);

CREATE TABLE Ovlada (
    id_u NUMERIC(7,0) NOT NULL,
    druh_zabavy VARCHAR(30) NOT NULL,
    CONSTRAINT PK_ovlada PRIMARY KEY (id_u,druh_zabavy),
    CONSTRAINT FK_ovlada_nazevzabavy FOREIGN KEY (druh_zabavy) REFERENCES Zabava,
    CONSTRAINT FK_ovlada_idu FOREIGN KEY (id_u) REFERENCES Bavic
);

CREATE TABLE Objednavka (
    id_o NUMERIC(7,0) NOT NULL,
    datum DATE,
    cas_objednani VARCHAR(5),
    cas_doruceni_do VARCHAR(5),
    delka_zabavy NUMERIC(3,0),
    zakaznik NUMERIC(7,0) NOT NULL,
    druh_zabavy VARCHAR(30),
    bavic NUMERIC(7,0),
    CONSTRAINT PK_objednavka_ido PRIMARY KEY (id_o),
    CONSTRAINT FK_objednavka_zakaznik FOREIGN KEY (zakaznik) REFERENCES Zakaznik,
    CONSTRAINT FK_objednavka_nazevzabavy FOREIGN KEY (druh_zabavy) REFERENCES Zabava,
    CONSTRAINT FK_objednavka_bavic FOREIGN KEY (bavic) REFERENCES Bavic
);

CREATE TABLE Obsahuje (
    jmeno_p VARCHAR(30) NOT NULL,
    id_p NUMERIC(7,0) NOT NULL,
    id_o NUMERIC(7,0) NOT NULL,
    pocet_kusu NUMERIC(3,0),
    CONSTRAINT PK_obsahuje PRIMARY KEY (jmeno_p,id_p,id_o),
    CONSTRAINT FK_obsahuje_jmenopidp FOREIGN KEY (jmeno_p,id_p) REFERENCES Druh(jmeno_p,id_p),
    CONSTRAINT FK_obsahuje_ido FOREIGN KEY (id_o) REFERENCES Objednavka
);

-- Uzivatel(id_uzivatele,jmeno,datum_narozeni,adresa)
INSERT INTO Uzivatel
VALUES(001,'Pavel Dostal', TO_DATE('10.10.1999','dd.mm.yyyy'),'Palackeho 5, Brno');
INSERT INTO Uzivatel 
VALUES(002,'David Nosek', TO_DATE('03.10.2000','dd.mm.yyyy'),'Filipa 90, Ostrava');
INSERT INTO Uzivatel
VALUES(003,'Jan Novák', TO_DATE('10.09.2001','dd.mm.yyyy'),'Komenskeho 38, Brno');
INSERT INTO Uzivatel
VALUES(004,'Ondra Dorman', TO_DATE('12.01.2003','dd.mm.yyyy'),'Kouce 38, Brno');
INSERT INTO Uzivatel
VALUES(005,'Denis Vasek', TO_DATE('20.11.1992','dd.mm.yyyy'),'Pottra 38, Brno');
INSERT INTO Uzivatel
VALUES(006,'Petr Sic', TO_DATE('19.02.1976','dd.mm.yyyy'),'Dobyho 38, Brno');
INSERT INTO Uzivatel
VALUES(007,'Vladimir Metar', TO_DATE('01.08.2000','dd.mm.yyyy'),'Flaminga 38, Brno');
INSERT INTO Uzivatel
VALUES(008,'Vladimir Metar ml.', TO_DATE('01.08.2010','dd.mm.yyyy'),'Flaminga 38, Brno');

-- Vlastnik(id_uzivatele,linkedin)
INSERT INTO Vlastnik
VALUES (001, 'PizzaStar');
INSERT INTO Vlastnik
VALUES (002, 'PizzaMaxi');

-- Zakaznik(id_uzivatele,adresa_doruceni)
INSERT INTO Zakaznik
VALUES (003, 'Komenskeho 38, Brno');
INSERT INTO Zakaznik
VALUES (004, 'Dalibora 8, Brno');
INSERT INTO Zakaznik
VALUES (005, 'Nemcove 23, Brno');

-- Bavic(id_uzivatele,nazev_sceny,zivotopis,cena)
INSERT INTO Bavic
VALUES (006,'Hopsani','bla bla bla', 300);
INSERT INTO Bavic
VALUES (007,'Skakani','BLA BLA BLA', 250);
INSERT INTO Bavic
VALUES (008,'Skakani','BLA BLA BLA', 150);

-- Pizzerie(id_pizzerie,nazev,ulice,mesto,psc,telefon,oteviraci_doba,id_vlasnika)
INSERT INTO Pizzerie
VALUES (111,'Pizza Star', 'Markova','Brno',89301,777777777,'24/7',001);
INSERT INTO Pizzerie
VALUES (333,'Pizza Maxi', 'Filipa','Brno',89301,999999999,'24/7',002);

-- Pracovnik(id_pizzerie,id_uzivatele,dostupnost)
INSERT INTO Pracovnik
VALUES (111,006,'Pondělí, Úterý, Čtvrtek');
INSERT INTO Pracovnik
VALUES (333,007,'Středa, Pátek, Sobota, Neděle');
INSERT INTO Pracovnik
VALUES (333,008,'Středa, Pátek, Sobota, Neděle');

-- Druh(jmeno_pizzy,obsahuje,cena,id_pizzerie)
INSERT INTO Druh
VALUES ('Margarita','Syr',200,111);
INSERT INTO Druh
VALUES ('Fungi','Houby',300,333);
INSERT INTO Druh
VALUES ('Salami','Salam',400,111);

-- Zabava(druh_zabavy)
INSERT INTO Zabava
VALUES ('Mimika');
INSERT INTO Zabava
VALUES ('Zpev');

-- Ovlada(id_uzivatele,druh_zabavy)
INSERT INTO Ovlada 
VALUES (006,'Mimika');
INSERT INTO Ovlada
VALUES (007,'Mimika');


-- Objednavka(id_objednavky,datum,cas_objednani,cas_doruceni_do,zakaznik,druh_zabavy,bavic)
INSERT INTO Objednavka
VALUES (222,TO_DATE('22.03.2002','dd.mm.yyyy'),'10:30','12:00',30,003,'Mimika',006);
INSERT INTO Objednavka
VALUES(444,TO_DATE('11.04.2022','dd.mm.yyyy'),'12:30','13:30',30,004,'Mimika',006);
INSERT INTO Objednavka
VALUES (555,TO_DATE('22.02.2022','dd.mm.yyyy'),'18:00','20:00',00,005,'Mimika',007);

-- Obsahuje(jmeno_pizzy,id_p,id_objednavky,pocet)
INSERT INTO Obsahuje
VALUES ('Margarita',111,222,10);
INSERT INTO Obsahuje
VALUES ('Fungi',333,222,2);
INSERT INTO Obsahuje
VALUES ('Salami',111,444,3);
INSERT INTO Obsahuje
VALUES ('Margarita',111,555,2);

COMMIT;

-- Uvažujte následující dotazy v jazyce SQL nad níže definovanými tabulkami.
-- Doplňte do tabulek záznamy tak, aby bylo možné otestovat správnost vypracovaných dotazů.
-- • Který zákazník si objednává z nějaké pizzerie pouze pizzu se zábavou a z jaké pizzerie to je? (jmeno, nazev, adresa)
-- • Po každého baviče zjistěte, kolik hodin celkem strávil zábavou nějakých zákazníků. Uvažujte i možnost, že některý z bavičů dosud nebavil žádného zákazníka. (jmeno, pocet_hodin)

SELECT * FROM Uzivatel;
SELECT * FROM Vlastnik;
SELECT * FROM Zakaznik;
SELECT * FROM Bavic;
SELECT * FROM Pizzerie;
SELECT * FROM Pracovnik;
SELECT * FROM Druh;
SELECT * FROM Zabava;
SELECT * FROM Ovlada;
SELECT * FROM Obsahuje;
SELECT * FROM Objednavka;

-- • Ve kterých pizzeriích si objednal pizzu pan Jan Novák? (nazev, adresa)
SELECT DISTINCT
    pizzerie.nazev,
    (pizzerie.ulice || ' ' || pizzerie.mesto || ' ' || pizzerie.psc) AS "ADRESA"
FROM Obsahuje
INNER JOIN Objednavka ON objednavka.id_o = obsahuje.id_o
INNER JOIN Pizzerie ON Obsahuje.id_p = pizzerie.id_p
INNER JOIN Uzivatel ON objednavka.zakaznik = uzivatel.id_u
WHERE uzivatel.jmeno = 'Jan Novák';

-- • Pro každou pizzerii a každý den v týdnu zjistěte, kteří baviči jsou dostupní během celé otvírací doby v daný den (nazev, adresa, den, jmeno)
WITH TEMP_DNY_A_BAVIC(DEN, BAVIC_ID) AS
(SELECT 'Pondělí' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Pondělí%'
  UNION
  SELECT 'Úterý' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Úterý%'
  UNION
  SELECT 'Středa' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Středa%'
  UNION
  SELECT 'Čtvrtek' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Čtvrtek%'
  UNION
  SELECT 'Pátek' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Pátek%'
  UNION
  SELECT 'Sobota' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Sobota%'
  UNION
  SELECT 'Neděle' AS den_v_tydnu, id_u FROM Pracovnik WHERE dostupnost LIKE '%Neděle%')

SELECT DISTINCT 
    pizzerie.nazev,
    (pizzerie.ulice || ' ' || pizzerie.mesto || ' ' || pizzerie.psc) AS "ADRESA",
    DEN,
    uzivatel.jmeno
FROM 
    TEMP_DNY_A_BAVIC
INNER JOIN Bavic ON BAVIC_ID = Bavic.id_u
INNER JOIN Pracovnik ON Bavic.id_u = Pracovnik.id_u
INNER JOIN Pizzerie ON pracovnik.id_p = pizzerie.id_p
INNER JOIN Uzivatel ON Bavic.id_u = Uzivatel.id_u
ORDER BY
    CASE 
        DEN
        WHEN 'Pondělí' THEN 1
        WHEN 'Úterý' THEN 2
        WHEN 'Středa' THEN 3
        WHEN 'Čtvrtek' THEN 4
        WHEN 'Pátek' THEN 5
        WHEN 'Sobota' THEN 6
        WHEN 'Neděle' THEN 7
    END;

-- • Která pizzerie má nejvíce různých zákazníků a kolik jich má? (nazev, adresa, pocet_zakazniku)
SELECT DISTINCT
    pizzerie.nazev,
    (pizzerie.ulice || ' ' || pizzerie.mesto || ' ' || pizzerie.psc) AS "ADRESA",
    COUNT(DISTINCT uzivatel.id_u) AS "Pocet_zakazniku"
FROM Obsahuje
INNER JOIN Objednavka ON objednavka.id_o = obsahuje.id_o
INNER JOIN Pizzerie ON Obsahuje.id_p = pizzerie.id_p
INNER JOIN Uzivatel ON objednavka.zakaznik = uzivatel.id_u
GROUP BY pizzerie.nazev, (pizzerie.ulice || ' ' || pizzerie.mesto || ' ' || pizzerie.psc);
ORDER BY "Pocet_zakazniku" DESC;

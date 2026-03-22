# Slutprojekt i Databaser

**Kurs:** Databaser
**Datum:** March 11, 2026

## Syfte och mål

Slutprojektet ger dig möjlighet att visa att du kan designa, implementera och optimera en databas baserat på ett verkligt scenario. Projektet ska ligga inom ramarna för alla kursens lärandemål (1–11), men bedömningen på VG-nivå fokuserar särskilt på mål 10 och 11:

* **(10)** Välja en lämplig databaslösning baserat på projektets behov
* **(11)** Designa och underhålla en databas för att säkerställa dataintegritet och säkerhet

Tidigare inlämningar får inte återanvändas. Du måste skapa en ny databasdesign.

---

## Krav på projektet

### Grundkrav (G-nivå)

* Designa en databas med minst tre sammanlänkade tabeller (t.ex. kunder, produkter, beställningar)
* Implementera i ett RDBMS (MySQL/PostgreSQL)
* Använd primär- och främmande nycklar
* Säkerställ dataintegritet (NOT NULL, CHECK, DEFAULT, FOREIGN KEY)
* Implementera minst en trigger
* Använd JOIN och GROUP BY i minst två SQL-frågor
* Motivera dina val i en **README.md**

---

### Utökade krav (VG-nivå)

* Allt från G-nivå +
* Välj SQL/NoSQL/hybrid och motivera
* Implementera Stored Procedure
* Implementera säkerhetsstrategi (GRANT/REVOKE)
* Analysera prestanda (t.ex. index)
* Extra funktioner är ett plus
* Ev. bygg en applikation (t.ex. Python)

---

## Projektidéer

### G-nivå: Bokningssystem

**Tabeller:**

* Kunder (KundID, Namn, E-post)
* Tjänster (TjänstID, Namn, Pris)
* Bokningar (BokningID, KundID, TjänstID, Datum)

**Krav:**

* Spara bokningar
* Validera datum (CHECK)
* Trigger för bekräftelse (logg)

---

### VG-nivå: E-handel

**Tabeller:**

* Kunder (KundID, Namn, E-post, Lösenord, Registreringsdatum)
* Produkter (ProduktID, Namn, Pris, Lagerstatus)
* Beställningar (OrderID, KundID, Datum, Totalbelopp)
* Orderrader (OrderradID, OrderID, ProduktID, Antal, Pris)

**Krav:**

* Uppdatera lager automatiskt (trigger/event)
* Stored procedure för försäljning
* Behörigheter (admin-only uppdatering)
* Extra: moln/NoSQL

---

## Redovisning

* Lämna in via GitHub
* README.md ska innehålla projektbeskrivning
* Presentation inför klass
* Förklara designval och säkerhet

**Deadline:** Ange datum (202x-xx-xx)

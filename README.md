# NHL-databas

*Slutprojekt i Databaser (YH25)*

**Gabriel Gustafsson & Carlos Johansson Bergqvist**

---

## Projektbeskrivning

I det här projektet har vi byggt en relationsdatabas för NHL-statistik. Syftet är att lagra data från matcher och använda den för att analysera hur spelare och lag presterar över tid.

Vi har valt att fokusera på statistik som:

* Mål
* Assist
* Poäng (goals + assists)
* Tacklingar (hits)
* Skott (shots)
* Utvisningsminuter (PIM)
* Speltid (TOI)
* +/-  (plus/minus)

Databasen är designad för att hantera flera säsonger, så att man kan jämföra spelare över tid.

---

## Val av databastyp

Vi valde en relationsdatabas eftersom projektet innehåller tydliga relationer mellan spelare, lag, matcher och säsonger. Datan behöver hög dataintegritet och struktur.

En relationsdatabas passar bra i detta projekt eftersom vi behöver:

* primärnycklar och främmande nycklar
* tydliga relationer mellan tabeller
* säkra och konsekventa datatyper
* SQL-frågor med `JOIN` och `GROUP BY`

Därför passar MySQL/PostgreSQL utmärkt för just denna lösning. Sen är de det vi lärde oss i skolan.

---

## Databasdesign

### Tabeller

Databasen består av följande huvudtabeller:

* **player** – information om spelare
* **team** – laginformation
* **season** – säsonger
* **game** – matcher
* **player_team_season** – koppling mellan spelare, lag och säsong
* **player_game_stats** – spelarstatistik per match
* **team_game_stats** – lagstatistik per match

---

## Relationer

* En spelare kan spela i flera lag över olika säsonger
* Ett lag deltar i flera matcher
* En match spelas mellan två lag
* Statistik lagras per spelare och match
* Statistik kan aggregeras per säsong med hjälp av `JOIN` och `GROUP BY`

---

## Dataintegritet

Databasen använder flera funktioner för att säkerställa dataintegritet:

* **PRIMARY KEY** för unika rader
* **FOREIGN KEY** för att säkerställa giltiga relationer mellan tabeller
* **NOT NULL** för obligatoriska fält
* **DEFAULT** där det är lämpligt
* eventuella **CHECK-villkor** för att begränsa ogiltiga värden

Syftet är att undvika inkonsekvent eller ogiltig data i databasen.

---

## Funktionalitet

### Triggers

Automatisk beräkning av poäng:

* `points = goals + assists`

Triggers körs vid:

* INSERT
* UPDATE

---

### Stored Procedure

```sql
CALL get_points_leaderboard_by_season(season_id);
```

Returnerar en leaderboard över spelare baserat på total poäng för en specifik säsong.

---

## Exempel på queries

### Poängliga

```sql
SELECT p.first_name, p.last_name, SUM(pgs.points) AS total_points
FROM player_game_stats pgs
JOIN player p ON p.player_id = pgs.player_id
JOIN game g ON g.game_id = pgs.game_id
WHERE g.season_id = 20232024
GROUP BY p.player_id
ORDER BY total_points DESC;
```

### Tacklingsliga

```sql
SELECT p.first_name, p.last_name, SUM(pgs.hits) AS total_hits
FROM player_game_stats pgs
JOIN player p ON p.player_id = pgs.player_id
JOIN game g ON g.game_id = pgs.game_id
WHERE g.season_id = 20232024
GROUP BY p.player_id
ORDER BY total_hits DESC;
```

Dessa queries visar hur databasen kan användas för att analysera statistik med hjälp av JOIN och GROUP BY.

---

## Prestanda

För att förbättra prestandan används index på kolumner som ofta förekommer i relationer och sökningar, till exempel player_id, team_id, game_id och season_id.

Det gör det lättare att köra sammanställningar och frågor effektivt när databasen växer.

---

## Säkerhet

Projektet innehåller en enkel rollbaserad säkerhetsstrategi där olika användare får olika behörigheter.

admin_user har full behörighet att läsa och ändra data
analyst_user har endast behörighet att läsa statistik

Detta hanteras med GRANT och REVOKE i filen security.sql.

```sql
GRANT ALL PRIVILEGES ON nhl_database.* TO 'admin_user'@'localhost';
GRANT SELECT ON nhl_database.* TO 'analyst_user'@'localhost';
REVOKE INSERT, UPDATE, DELETE ON nhl_database.* FROM 'analyst_user'@'localhost';
```

Säkerheten testades i MySQL Workbench genom att skapa separata anslutningar för admin_user och analyst_user. Administratören kunde ändra data, medan analytikern endast kunde läsa statistik.

---

## Testdata

Projektet innehåller testdata för:

* 2 lag
* 1 säsong
* 4 spelare
* 1 match
* Spelar- och lagstatistik kopplad till matchen

---

## ER-diagram

Databasens struktur visas här:

![ER-diagram](/images/Databas-projekt.drawio.png)

---

## Lärdomar

Genom projektet har vi fått mer erfarenhet av att:

* Designa en relationsdatabas
* Arbeta med dataintegritet
* Använda triggers och stored procedures
* Optimera queries med index
* Tänka på säkerhet och behörigheter

---

## Möjlig vidareutveckling

* Bygga en webbapplikation ovanpå databasen
* Hämta live-data via NHL API
* Visualisering av data
* Avancerad statistik (t.ex. Corsi, xG)

---

## Filer i projektet

* `README.md` – projektbeskrivning
* `docs/assignment.md` – uppgiftsbeskrivning
* `images/Databas-projekt.drawio.png` – ER-diagram

### Databasfiler

* `database/schema.sql` – tabeller
* `database/triggers.sql` – triggers
* `database/procedures.sql` – stored procedures
* `database/seed.sql` – testdata
* `database/queries.sql` – exempel på queries
* `database/security.sql` – användare och behörigheter
* `database/nhl_database.sql` – komplett script

---

## Hur man kör projektet

1. Kör `schema.sql` för att skapa tabeller
2. Kör `triggers.sql`
3. Kör `procedures.sql`
4. Kör `seed.sql` för att lägga in testdata
5. Kör `security.sql` för att skapa användare och behörigheter
6. Kör `queries.sql` eller anropa stored procedures

Exempel:

```sql
CALL get_points_leaderboard_by_season(20232024);
```

---

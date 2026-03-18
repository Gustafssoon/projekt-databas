# NHL-databas

*Slutprojekt i Databaser (YH25)*

**Gabriel Gustafsson & Carlos Johansson Bergqvist**

---

## Projektbeskrivning

I det här projektet har vi byggt en relationsdatabas för NHL-statistik. Tanken är att kunna lagra data från matcher och sedan använda den för att analysera hur spelare presterar.

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
* En match spelas mellan två lag
* Statistik lagras per spelare och match
* Statistik aggregeras per säsong med hjälp av JOINs och GROUP BY i queries

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

* Erfarenhet av att designa och implementera en större relationsdatabas
* Fördjupad förståelse för triggers och hur de används för dataintegritet
* Stored procedures för återanvändbar logik
* Användning av index för att optimera prestanda vid queries

---

## Möjlig vidareutveckling

* Bygga en webbapplikation (frontend + API)
* Importera live-data via NHL API
* Visualisering av data
* Avancerad statistik (t.ex. Corsi, xG)

---

## Filer i projektet

* `README.md` – projektbeskrivning
* `images/Databas-projekt.drawio.png` – ER-diagram

### Databasfiler

* `database/schema.sql` – CREATE TABLE-satser
* `database/triggers.sql` – triggers
* `database/procedures.sql` – stored procedures
* `database/seed.sql` – testdata (INSERT)
* `database/queries.sql` – exempel på queries
* `database/nhl_database.sql` – komplett script (alla delar i en fil)

---

## Hur man kör projektet

1. Kör `schema.sql` för att skapa tabeller
2. Kör `triggers.sql`
3. Kör `procedures.sql`
4. Kör `seed.sql` för att lägga in testdata
5. Kör `queries.sql` eller anropa stored procedures

Exempel:

```sql
CALL get_points_leaderboard_by_season(20232024);
```

---

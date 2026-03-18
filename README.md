# 📃 NHL-databas

*Slutprojekt i Databaser (YH25)*

**Gabriel Gustafsson & Carlos Johansson Bergqvist**

---

## Projektbeskrivning

Detta projekt syftar till att modellera och implementera en relationsdatabas för NHL-statistik. Databasen är designad för att hantera data från matcher och lagra detaljerad spelar- och lagstatistik.

Fokus ligger på att möjliggöra analys av prestationer över tid, som till exempel:

* Mål
* Assist
* Poäng (goals + assists)
* Tacklingar (hits)
* Skott (shots)
* Utvisningsminuter (PIM)
* Speltid (TOI)
* +/-  (plus/minus)

Databasen stödjer även historisk data, vilket gör det möjligt att jämföra spelare mellan olika säsonger.

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
* Statistik aggregeras per säsong via queries

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

Returnerar en leaderboard över spelare baserat på total poäng för en given säsong.

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

### Tacklingar (hits leaderboard)

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
* Statistik för både spelare och lag

---

## ER-diagram

Databasens struktur illustreras här:

![ER-diagram](Databas-projekt.drawio.png)

---

## Lärdomar

* Design av relationsdatabaser och normalisering
* Hantering av many-to-many-relationer
* Användning av triggers för dataintegritet
* Stored procedures för återanvändbar logik
* Indexering för prestanda

---

## Möjlig vidareutveckling

* Bygga en webbapplikation (frontend + API)
* Importera live-data via NHL API
* Visualisering av data
* Avancerad statistik (t.ex. Corsi, xG)

---

## Filer i projektet

* `README.md`
* `Databas-projekt.drawio.png`
* `nhl_database.sql`

---

### 🚧 Status

**Work in progress**

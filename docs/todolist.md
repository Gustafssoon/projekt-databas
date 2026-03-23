# TO-DO LIST


## Planned
- [ ] Lägga till bilder på spelare i frontend
- [ ] Visa `headshots_url` i spelarvyer och API-svar
- [ ] Lägga till `relationship()` mellan modeller i SQLAlchemy  -- https://chatgpt.com/s/t_69c11638aa54819184ee5e51d33a6181
- [ ] Ta bort manuell generering av primärnycklar i importflödet  -- https://chatgpt.com/s/t_69c102ed26bc8191bb5fa752d511b487
- [ ] Göra importerna mer atomära genom att minska antalet `commit()`  -- https://chatgpt.com/s/t_69c1035129c8819195a2572d4fd9653c
- [ ] Lägga till bättre felhantering för NHL API-anrop  -- https://chatgpt.com/s/t_69c1039706608191b10d5aa4a2658214
- [ ] Rätta `map_team()` så att `city` inte använder `triCode`  -- https://chatgpt.com/s/t_69c103cef4fc819191bf835b9426235b
- [ ] Byta ut `print()` mot logging  -- https://chatgpt.com/s/t_69c115d162a081918d7c74d65e9cc05f
- [ ] Skydda adminpanelen med autentisering  -- https://chatgpt.com/s/t_69c100328938819187e62f82e66b433b
- [ ] Utöka `.gitignore` med fler vanliga Python-filer/mappa  -- https://chatgpt.com/s/t_69c1015d72488191a5b378e97d37340d
- [ ] Skriva tester för mappers och import services  -- https://chatgpt.com/s/t_69c1167750688191af6e0b25d923b499

## In Progress

- [ ] Koppla spelarbilder till databasen och resten av applikationen
- [ ] Städa upp importlogiken för spelare, lag, matcher och statistik
- [ ] Se över datamodellen för bättre relationer och stabilare migrationer

## Done ✓

- [x] Lagt till `headshots_url` i `schema.sql`
- [x] Uppdaterat README för att förklara hur man kör backend
- [x] Satt upp Flask app factory
- [x] Lagt till `extensions.py` för databas och migrationer
- [x] Skapat modeller för spelare, lag, säsonger, matcher och statistik
- [x] Implementerat grundläggande import från NHL API
- [x] Skapat första Alembic-migrationen för NHL-modeller
- [x] Lagt till adminvy med Flask-Admin
- [x] Tagit bort `start_date` och `end_date` från `player_team_season` och synkat migrationen
- [x] Lagt till sortering i `import_season_stats_limited()`

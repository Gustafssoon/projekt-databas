# TO-DO LIST

Vad vi planerar samt håller på att tillämpa:

### Todo

- [ ] Lägga till bilder på spelare i frontend
- [ ] Visa `headshots_url` i spelarvyer och API-svar
- [ ] Lägga till `relationship()` mellan modeller i SQLAlchemy
- [ ] Ta bort manuell generering av primärnycklar i importflödet
- [ ] Göra importerna mer atomära genom att minska antalet `commit()`
- [ ] Lägga till bättre felhantering för NHL API-anrop
- [ ] Rätta `map_team()` så att `city` inte använder `triCode`
- [ ] Synka modellen `PlayerTeamSeason` med migrationen
- [ ] Lägga till sortering i `import_season_stats_limited()`
- [ ] Byta ut `print()` mot logging
- [ ] Skydda adminpanelen med autentisering
- [ ] Utöka `.gitignore` med fler vanliga Python-filer/mappar
- [ ] Skriva tester för mappers och import services

### In Progress

- [ ] Koppla spelarbilder till databasen och resten av applikationen
- [ ] Städa upp importlogiken för spelare, lag, matcher och statistik
- [ ] Se över datamodellen för bättre relationer och stabilare migrationer

### Done ✓

- [x] Lagt till `headshots_url` i `schema.sql`
- [x] Uppdaterat README för att förklara hur man kör backend
- [x] Satt upp Flask app factory
- [x] Lagt till `extensions.py` för databas och migrationer
- [x] Skapat modeller för spelare, lag, säsonger, matcher och statistik
- [x] Implementerat grundläggande import från NHL API
- [x] Skapat första Alembic-migrationen för NHL-modeller
- [x] Lagt till adminvy med Flask-Admin

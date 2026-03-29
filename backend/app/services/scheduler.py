import os
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def start_scheduler(app):
    print("start_scheduler called")
    print("WERKZEUG_RUN_MAIN =", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("app.debug =", app.debug)

    if app.debug and os.environ.get("WERKZEUG_RUN_MAIN") == "false":
        print("Skipping scheduler in reloader parent process")
        return

    if scheduler.running:
        print("Scheduler already running")
        return

    def refresh_team(team_code: str):
        with app.app_context():
            from app.services.import_service import refresh_recent_games_for_team

            print(f"--- Scheduler job for {team_code} ---")
            stats_result = refresh_recent_games_for_team(
                team_code, 20252026, limit=3
            )
            print(f"{team_code} stats refreshed:", stats_result)

    def job():
        refresh_team("TOR")
        refresh_team("MTL")

    scheduler.add_job(
        job,
        trigger="interval",
        minutes=5,
        id="refresh_recent_games_job",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()
    print("✅ Scheduler started")

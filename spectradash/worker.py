import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from spectradash.config import load_config
from spectradash.jobs import render_and_show

logging.basicConfig(level=logging.INFO)

def refresh():
    try:
        config = load_config()
        if config.auto_refresh:
            render_and_show()
    except Exception:
        logging.exception("Scheduled refresh failed")

def main():
    config = load_config()
    scheduler = BlockingScheduler()
    scheduler.add_job(
        refresh,
        "interval",
        minutes=max(3, config.refresh_minutes),
        id="display-refresh",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )
    refresh()
    scheduler.start()

if __name__ == "__main__":
    main()

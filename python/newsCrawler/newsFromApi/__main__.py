import time
from datetime import datetime
from os import makedirs

import click
import schedule
from dynaconf import settings

from news import News
from ckip import CKIP

DATA_PATH = settings.DATA_PATH
TARGETS = settings.NEWS_TARGETS
NEWS_DAYS = settings.NEWS_DAYS
API_KEY = settings.API_KEY
SCHEDULE_MINUTES = settings.SCHEDULE_MINUTES
RUN_AFTER_MINUTES = settings.SCHEDULE_MINUTES


def heart_beat():
    print(f"Alive at {datetime.now()}")


def run():
    crawler = News()
    print("News targets", TARGETS)
    makedirs(DATA_PATH, exist_ok=True)
    for target in TARGETS:
        print("News target", target)
        crawler.getNewsFromAPI(target, NEWS_DAYS, API_KEY, DATA_PATH)


def download_ckip():
    ckip = CKIP()
    print("Download CKIP....")
    ckip.download_CKIP()


@click.command()
@click.option("-s", "--schedule_arg", is_flag=True, help="run every 30 minutes")
def main(schedule_arg):
    # 開始執行後，先下載CKIP
    download_ckip()

    if schedule_arg is True:
        schedule.every(480).minutes.do(run)
        schedule.every().minutes.do(heart_beat)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        run()


if __name__ == "__main__":
    main()

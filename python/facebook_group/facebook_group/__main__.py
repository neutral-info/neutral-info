
import time
from datetime import datetime
from os import makedirs

import click
import schedule
from dynaconf import settings

from facebook_group import FacebookGroupCrawler

DATA_PATH = settings.DATA_PATH
TARGETS = settings.GROUP_TARGETS


def heart_beat():
    print(f"Alive at {datetime.now()}")


def run():
    crawler = FacebookGroupCrawler()
    print('Facebook group targets', TARGETS)
    makedirs(DATA_PATH, exist_ok=True)
    for target in TARGETS:
        crawler.start_Crawler(target, DATA_PATH)


@click.command()
@click.option('-s', '--schedule_arg', is_flag=True, help="run every 30 minutes")
def main(schedule_arg):
    if schedule_arg is True:
        schedule.every(30).minutes.do(run)
        schedule.every().minutes.do(heart_beat)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        run()


if __name__ == "__main__":
    main()

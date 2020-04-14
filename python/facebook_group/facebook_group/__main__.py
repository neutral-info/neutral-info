
import time
from datetime import datetime
from os import makedirs

import click
import schedule

from facebook_group import FacebookGroupCrawler

DATA_PATH = "./data"


def heart_beat():
    print(f"Alive at {datetime.now()}")


def run():
    crawler = FacebookGroupCrawler()
    makedirs(DATA_PATH, exist_ok=True)
    crawler.start_Crawler('2065219296931017', DATA_PATH)


@click.command()
@click.option('-s', '--schedule_arg', is_flag=True, help="run every 2 hours")
def main(schedule_arg):
    if schedule_arg is True:
        schedule.every(2).hours.do(run)
        schedule.every().minutes.do(heart_beat)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        run()


if __name__ == "__main__":
    main()

import time
from datetime import datetime
from os import makedirs

import click
import schedule

DATA_PATH = "./data"


def heart_beat():
    print(f"Alive at {datetime.now()}")


def run():
    makedirs(DATA_PATH, exist_ok=True)


@click.command()
@click.option("-s", "--schedule_arg", is_flag=True, help="run every 2 hours")
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

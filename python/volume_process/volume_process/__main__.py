import time
from datetime import datetime
from os import makedirs

import click
import schedule

from volume_process import Volume


def heart_beat():
    print(f"Alive at {datetime.now()}")


def run():
    # 處理
    volume = Volume()
    volume.calculate_volume()
    volume.calculate_bomb()


@click.command()
@click.option("-s", "--schedule_arg", is_flag=True, help="run every 12 hours")
def main(schedule_arg):
    if schedule_arg is True:
        schedule.every(12).hours.do(run)
        schedule.every().minutes.do(heart_beat)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        run()


if __name__ == "__main__":
    main()

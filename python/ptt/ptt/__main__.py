import time
from datetime import datetime
from os import makedirs

import click
import schedule

from crawler import PttWebCrawler

DATA_PATH = "./data"


def heart_beat():
    print(f"Alive at {datetime.now()}")


def run():
    # 爬蟲抓取了四個板：Gossiping、Stock、C_Chat、HatePolitics
    crawler = PttWebCrawler(as_lib=True)
    Gossiping_last_page = crawler.getLastPage("Gossiping")
    Stock_last_page = crawler.getLastPage("Stock")
    C_Chat_last_page = crawler.getLastPage("C_Chat")
    HatePolitics_last_page = crawler.getLastPage("HatePolitics")
    makedirs(DATA_PATH, exist_ok=True)
    print("Processing Gossiping")
    crawler.parse_articles(
        Gossiping_last_page - 100, Gossiping_last_page, "Gossiping", path=DATA_PATH
    )
    print("Processing Stock")
    crawler.parse_articles(
        Stock_last_page - 10, Stock_last_page, "Stock", path=DATA_PATH
    )
    print("Processing C_Chat")
    crawler.parse_articles(
        C_Chat_last_page - 20, C_Chat_last_page, "C_Chat", path=DATA_PATH
    )
    print("Processing HatePolitics")
    crawler.parse_articles(
        HatePolitics_last_page - 20,
        HatePolitics_last_page,
        "HatePolitics",
        path=DATA_PATH,
    )


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

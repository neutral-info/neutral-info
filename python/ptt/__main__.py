
from crawler import PttWebCrawler


def main():
    crawler = PttWebCrawler(as_lib=True)
    crawler.parse_articles(100, 101, "PublicServan")


if __name__ == "__main__":
    main()

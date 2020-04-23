from glob import glob
from dataclasses import dataclass
from typing import List
import json

NEWS_COMPANY = [
    "cna.com.tw",  # 中央社
    "tvbs.com.tw",  # TVBS
    "ettoday.net",  # ETToday
    "chinatimes.com",  # 中時電子報
    "udn.com",  # UDN
    "epochtimes.com",  # 大紀元
    "nownews.com",  # 今日新聞
    "setn.com",  # 三立
    "ltn.com.tw",  # 自由
    "upmedia.mg",  # 上報
    "pts.org.tw",  # 公視
]


@dataclass
class MessageCount:
    all: int
    count: int
    boo: int
    neutral: int
    push: int


@dataclass
class Message:
    push_countent: str
    push_ipdatetime: str
    push_tag: str
    push_userid: str


@dataclass
class Articles:
    article_id: str
    article_title: str
    author: str
    board: str
    content: str
    date: str
    ip: str
    url: str
    message_count: MessageCount
    messages: List[Message]


if __name__ == "__main__":
    paths = glob("data/*.log")
    articles = []
    for path in paths:
        with open(path) as fp:
            articles += fp.readlines()
    for i, article_log in enumerate(articles):
        for company in NEWS_COMPANY:
            article = json.loads(article_log)
            if company in article["content"]:
                print(f"news company in context, id: {i}, company: {company}")
                with open(f"data/separated/{company}.log", "a") as fp:
                    fp.write(article_log)

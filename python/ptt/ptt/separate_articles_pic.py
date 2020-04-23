from glob import glob
from dataclasses import dataclass
from typing import List
import json

PIC_EXTENSIONS = [".jpg", ".png", ".gif"]


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
        for ext in PIC_EXTENSIONS:
            article = json.loads(article_log)
            if ext in article["content"]:
                print(f"picture in context, id: {i}")
                with open(f"data/separated/content.log", "a") as fp:
                    fp.write(article_log)
            for msg in article["messages"]:
                if ext in msg["push_content"]:
                    print(f"picture in msg, id: {i}")
                    with open(f"data/separated/message.log", "a") as fp:
                        fp.write(article_log)
                    break

# coding=utf-8
from __future__ import absolute_import, print_function

import argparse
import codecs
import json
import os
import re
import time
import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from dynaconf import settings

__version__ = "1.0"

VERIFY = True

DBSRV_IP = settings.DBSRV_IP
DBSRV_PORT = settings.DBSRV_PORT
DBSRV_USERNAME = settings.DBSRV_USERNAME
DBSRV_PASSWORD = settings.DBSRV_PASSWORD
DBSRV_SCHEMA = settings.DBSRV_SCHEMA
DBSRV_PTT_TABLE = settings.DBSRV_PTT_TABLE

# 初始化資料庫連線，使用pymysql模組
engine = create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(
        DBSRV_USERNAME,
        DBSRV_PASSWORD,
        DBSRV_IP,
        DBSRV_PORT,
        DBSRV_SCHEMA,
    )
)


class PttWebCrawler(object):

    PTT_URL = "https://www.ptt.cc"

    """docstring for PttWebCrawler"""

    def __init__(self, cmdline=None, as_lib=False):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""
            A crawler for the web version of PTT, the largest online community in Taiwan.
            Input: board name and page indices (or articla ID)
            Output: BOARD_NAME-START_INDEX-END_INDEX.json (or BOARD_NAME-ID.json)
        """,
        )
        parser.add_argument(
            "-b", metavar="BOARD_NAME", help="Board name", required=True
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-i",
            metavar=("START_INDEX", "END_INDEX"),
            type=int,
            nargs=2,
            help="Start and end index",
        )
        group.add_argument("-a", metavar="ARTICLE_ID", help="Article ID")
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + __version__
        )

        if not as_lib:
            if cmdline:
                args = parser.parse_args(cmdline)
            else:
                args = parser.parse_args()
            board = args.b
            if args.i:
                start = args.i[0]
                if args.i[1] == -1:
                    end = self.getLastPage(board)
                else:
                    end = args.i[1]
                self.parse_articles(start, end, board)
            else:  # args.a
                article_id = args.a
                self.parse_article(article_id, board)

    def parse_articles(self, start, end, board, path=".", timeout=3):
        filename = board + "-" + str(start) + "-" + str(end) + ".log"
        filename = os.path.join(path, filename)
        print("filename", filename)
        for i in range(end - start + 1):
            index = start + i
            print(
                "Processing index:",
                str(index),
                self.PTT_URL + "/bbs/" + board + "/index" + str(index) + ".html",
            )
            resp = requests.get(
                url=self.PTT_URL + "/bbs/" + board + "/index" + str(index) + ".html",
                cookies={"over18": "1"},
                verify=VERIFY,
                timeout=timeout,
            )
            if resp.status_code != 200:
                print("invalid url:", resp.url)
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            divs = soup.find_all("div", "r-ent")
            for div in divs:
                try:
                    # ex. link would be <a href="/bbs/PublicServan/M.1127742013.A.240.html">Re: [問題] 職等</a>
                    href = div.find("a")["href"]
                    link = self.PTT_URL + href
                    article_id = re.sub(r"\.html", "", href.split("/")[-1])
                    # 原本採寫出檔案的方式，目前直接改以直接寫入資料庫
                    if div == divs[-1] and i == end - start:  # last div of last page
                        # self.store(filename, self.parse(link, article_id, board), "a")
                        self.parse(link, article_id, board)
                    else:
                        # self.store(filename, self.parse(link, article_id, board), "a")
                        self.parse(link, article_id, board)
                except Exception as e:
                    print(e.args[0])
                    pass
            time.sleep(0.1)
        return filename

    def parse_article(self, article_id, board, path="."):
        link = self.PTT_URL + "/bbs/" + board + "/" + article_id + ".html"
        filename = board + "-" + article_id + ".json"
        filename = os.path.join(path, filename)
        # 原本採寫出檔案的方式，目前直接改以直接寫入資料庫
        # self.store(filename, self.parse(link, article_id, board), "w")
        self.parse(link, article_id, board)
        return filename

    @staticmethod
    def parse(link, article_id, board, timeout=3):
        print("Processing article:", article_id)
        resp = requests.get(
            url=link, cookies={"over18": "1"}, verify=VERIFY, timeout=timeout
        )
        if resp.status_code != 200:
            print("invalid url:", resp.url)
            return json.dumps(
                {"error": "invalid url"}, sort_keys=True, ensure_ascii=False
            )
        soup = BeautifulSoup(resp.text, "html.parser")
        main_content = soup.find(id="main-content")
        metas = main_content.select("div.article-metaline")
        author = ""
        title = ""
        date = ""
        if metas:
            author = (
                metas[0].select("span.article-meta-value")[0].string
                if metas[0].select("span.article-meta-value")[0]
                else author
            )
            title = (
                metas[1].select("span.article-meta-value")[0].string
                if metas[1].select("span.article-meta-value")[0]
                else title
            )
            date = (
                metas[2].select("span.article-meta-value")[0].string
                if metas[2].select("span.article-meta-value")[0]
                else date
            )

            # remove meta nodes
            for meta in metas:
                meta.extract()
            for meta in main_content.select("div.article-metaline-right"):
                meta.extract()

        # remove and keep push nodes
        pushes = main_content.find_all("div", class_="push")
        for push in pushes:
            push.extract()

        try:
            ip = main_content.find(text=re.compile("※ 發信站:"))
            ip = re.search(r"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*", ip).group()
        except Exception:
            ip = "None"

        # 移除 '※ 發信站:' (starts with u'\u203b'), '◆ From:' (starts with u'\u25c6'), 空行及多餘空白
        # 保留英數字, 中文及中文標點, 網址, 部分特殊符號
        filtered = [
            v
            for v in main_content.stripped_strings
            if v[0] not in ["※", "◆"] and v[:2] not in ["--"]
        ]
        expr = re.compile(
            r"[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]"
        )
        for i in range(len(filtered)):
            filtered[i] = re.sub(expr, "", filtered[i])

        filtered = [_f for _f in filtered if _f]  # remove empty strings
        filtered = [
            x for x in filtered if article_id not in x
        ]  # remove last line containing the url of the article
        content = " ".join(filtered)
        content = re.sub(r"(\s)+", " ", content)
        # print 'content', content

        # push messages
        p, b, n = 0, 0, 0
        messages = []
        for push in pushes:
            if not push.find("span", "push-tag"):
                continue
            push_tag = push.find("span", "push-tag").string.strip(" \t\n\r")
            push_userid = push.find("span", "push-userid").string.strip(" \t\n\r")
            # if find is None: find().strings -> list -> ' '.join; else the current way
            push_content = push.find("span", "push-content").strings
            push_content = " ".join(push_content)[1:].strip(" \t\n\r")  # remove ':'
            push_ipdatetime = push.find("span", "push-ipdatetime").string.strip(
                " \t\n\r"
            )
            messages.append(
                {
                    "push_tag": push_tag,
                    "push_userid": push_userid,
                    "push_content": push_content,
                    "push_ipdatetime": push_ipdatetime,
                }
            )
            if push_tag == "推":
                p += 1
            elif push_tag == "噓":
                b += 1
            else:
                n += 1

        # count: 推噓文相抵後的數量; all: 推文總數
        message_count = {
            "all": p + b + n,
            "count": p - b,
            "push": p,
            "boo": b,
            "neutral": n,
        }

        # print("msgs", messages)
        # print 'mscounts', message_count

        # json data
        # 補上crawler抓取資料的觸發時間，以便後續計算聲量使用
        data = {
            "url": link,
            "board": board,
            "article_id": article_id,
            "article_title": title,
            "author": author,
            "date": date,
            "content": content,
            "ip": ip,
            "message_count": message_count,
            "messages": messages,
            "triger_time": datetime.datetime.now().astimezone().isoformat(),
        }

        # Messages的部分，也一併保留
        data_simple = {
            "article_id": article_id,
            "article_title": title,
            "author": author,
            "board": board,
            "content": content,
            "date": date,
            "ip": ip,
            "messages": json.dumps(messages, ensure_ascii=False),
            "url": link,
            "message_count.all": message_count["all"],
            "message_count.boo": message_count["boo"],
            "message_count.count": message_count["count"],
            "message_count.neutral": message_count["neutral"],
            "message_count.push": message_count["push"],
            "triger_time": datetime.datetime.now().astimezone().isoformat(),
        }
        # print 'original:', d

        with engine.connect() as conn:

            # 原本PTT爬蟲資料採重覆新增，不過考量因將回文內容也納入蒐集後，
            # 所需空間快速增加：因此調整成會先判斷該筆貼文是否已存在，
            # 如以存在就採更新同一筆，如無則新增一筆

            query_ptt = """ select * from ptt p where p.article_id = %s """
            rs_ptt = conn.execute(query_ptt, str(article_id))

            if rs_ptt and rs_ptt.rowcount:
                for row in rs_ptt:
                    print(
                        f"update count from:{ row['message_count.all']}, to:{message_count['all']}"
                    )
                    update_ptt = """ update ptt SET messages = %s, \
                                                    `message_count.all` = %s, \
                                                    `message_count.boo` = %s, \
                                                    `message_count.count` = %s, \
                                                    `message_count.neutral` = %s, \
                                                    `message_count.push` = %s, \
                                                    triger_time = %s \
                                    where article_id = %s """
                    rs_ptt = conn.execute(
                        update_ptt,
                        json.dumps(messages, ensure_ascii=False),
                        message_count["all"],
                        message_count["boo"],
                        message_count["count"],
                        message_count["neutral"],
                        message_count["push"],
                        datetime.datetime.now().astimezone().isoformat(),
                        str(article_id),
                    )
            else:
                # ptt貼文資料寫入資料庫
                dfPTT = pd.DataFrame(data_simple, index=[0])
                dfPTT.to_sql(
                    DBSRV_PTT_TABLE,
                    con=engine,
                    if_exists="append",
                    index=False,
                )

        return json.dumps(data, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def getLastPage(board, timeout=3):
        content = requests.get(
            url="https://www.ptt.cc/bbs/" + board + "/index.html",
            cookies={"over18": "1"},
            timeout=timeout,
        ).content.decode("utf-8")
        first_page = re.search(
            r'href="/bbs/' + board + r'/index(\d+).html">&lsaquo;', content
        )
        if first_page is None:
            return 1
        return int(first_page.group(1)) + 1

    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding="utf-8") as f:
            f.write(data + "\n")

    @staticmethod
    def get(filename, mode="r"):
        with codecs.open(filename, mode, encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":
    c = PttWebCrawler()

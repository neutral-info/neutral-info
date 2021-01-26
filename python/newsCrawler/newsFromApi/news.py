import uuid
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from sqlalchemy import create_engine
from dynaconf import settings
from ckiptagger import WS, POS, NER
from random import randint

DBSRV_IP = settings.DBSRV_IP
DBSRV_PORT = settings.DBSRV_PORT
DBSRV_USERNAME = settings.DBSRV_USERNAME
DBSRV_PASSWORD = settings.DBSRV_PASSWORD
DBSRV_SCHEMA = settings.DBSRV_SCHEMA
DBSRV_NEWS_TABLE = settings.DBSRV_NEWS_TABLE
DBSRV_VOLUME_TABLE = settings.DBSRV_VOLUME_TABLE


class News(object):
    """News from News api: https://newsapi.org/docs/client-libraries/python"""

    # def __init__(self):
    # /v2/everything
    # for newsTarget in self.newsTargets:
    #     self.getNewsFromAPI(newsTarget, self.news_days)

    def getNewsFromAPI(self, target: str, days: int, apiKey: str, data_path: str):
        # print(
        #     "News target:{}, days:{}, apiKey:{}, data_path:{}".format(
        #         target, days, apiKey, data_path
        #     )
        # )
        if days is not None:
            newsapi = NewsApiClient(api_key=apiKey)

            # 初始化CKIP詞庫
            ws = WS("./data")
            pos = POS("./data")
            ner = NER("./data")

            if type(days) == int:
                if days > 0:
                    # 往前追溯幾天
                    for i in range(0, days):
                        queryday = datetime.now() - timedelta(i)
                        strQueryday = datetime.strftime(queryday, "%Y-%m-%d")

                        # print(
                        #     "News target:{}, from_param:{}, to:{}".format(
                        #         target, strQueryday, strQueryday
                        #     )
                        # )

                        all_articles: dict = newsapi.get_everything(
                            # q="bitcoin",
                            # sources="bbc-news,the-verge",
                            domains=target,
                            from_param=strQueryday,
                            to=strQueryday,
                            page_size=100,
                            # language="en",
                            # sort_by="relevancy",
                            # page=1,
                        )

                        # 印出整個object，並讓它易讀
                        # pp = pprint.PrettyPrinter(indent=4)
                        # pp.pprint(all_articles)
                        # print(all_articles)

                        # parsed = json.loads(str(all_articles["articles"]))
                        # print(json.dumps(parsed, indent=4, sort_keys=True))

                        if all_articles["totalResults"] > 0:
                            # 印出目前抓到哪一個單位，以及執行狀況及筆數
                            print(
                                "---date: {} ------news target: {} ---status: {} -----get: {} --------------".format(
                                    strQueryday,
                                    target,
                                    all_articles["status"],
                                    all_articles["totalResults"],
                                )
                            )

                            for article in all_articles["articles"]:
                                # print(article["title"])
                                print(article["url"])

                            df = pd.DataFrame(all_articles["articles"])
                            # print(df)

                            # 透過URL辨識為唯一值
                            urls = df["url"].unique()
                            for url in urls:
                                df.loc[df["url"] == url, "newsuuid"] = uuid.uuid4().hex
                                df.loc[df["url"] == url, "source"] = target

                                # 截取出新聞標題中的關鍵字
                                news_title = df.loc[
                                    df["url"] == url, "title"
                                ].to_string(index=False)
                                news_title = news_title + df.loc[
                                    df["url"] == url, "description"
                                ].to_string(index=False)
                                print(news_title)

                                # 將新聞內容進行解析
                                ws_results = ws([news_title])
                                pos_results = pos(ws_results)
                                ner_results = ner(ws_results, pos_results)

                                # 將解析出來的字轉成特定陣列
                                news_keywords = []
                                for name in ner_results[0]:
                                    # print(name[3])
                                    news_keywords.append(name[3])

                                # 去除重覆的關鍵字，並轉成特定關鍵字字串
                                strNews_keywords = ",".join(
                                    list(dict.fromkeys(news_keywords))
                                )
                                print(f"keyword:{strNews_keywords}")
                                df.loc[df["url"] == url, "keywords"] = strNews_keywords

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

                            # 新聞主體資料寫入資料庫
                            df.to_sql(
                                DBSRV_NEWS_TABLE,
                                con=engine,
                                if_exists="append",
                                index=False,
                            )

                else:
                    raise ValueError("page param should be an int greater than 0")
            else:
                raise TypeError("page param should be an int")

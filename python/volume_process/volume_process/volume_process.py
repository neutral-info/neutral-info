# -*-coding:utf-8 -*-

# read as csv
import pandas as pd
from sqlalchemy import create_engine
from dynaconf import settings

# 從setting.toml中讀取資料庫相關設定
DBSRV_IP = settings.DBSRV_IP
DBSRV_PORT = settings.DBSRV_PORT
DBSRV_USERNAME = settings.DBSRV_USERNAME
DBSRV_PASSWORD = settings.DBSRV_PASSWORD
DBSRV_SCHEMA = settings.DBSRV_SCHEMA
DBSRV_VOLUME_TABLE = settings.DBSRV_VOLUME_TABLE


class Volume(object):
    """聲量相關處理"""

    def calculate_volume(self):

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

        conn = engine.connect()

        # 檢索近14天的新聞，註：時間控制在view上，降低系統操作負擔
        queryNewsList = "select newsuuid, \
                            SUBSTRING_INDEX(SUBSTRING_INDEX(title, ' - ', 1), '｜ ', 1) as title, \
                            url \
                        from news_lastpost nfa"

        # 取得新聞清單
        dfNewsList = pd.read_sql(sql=queryNewsList, con=conn)  # mysql query
        lendfNewsList: int = len(dfNewsList)

        # 用來儲存 news 聲量
        newsVolume: dict = {
            "newsuuid": [],
            "volume_now": [],
            "ptt_volume": [],
            "fb_fanpage_volume": [],
        }

        # print(generator_df)
        for index, dfNewsRow in dfNewsList.iterrows():

            # 檢查該新聞聞是否出現在Ptt中
            queryNewsInPtt = """
                select * from ptt_lastpost p where p.content like %s or p.content like %s
            """

            # 檢查該新聞聞是否出現在fanpage中
            queryNewsInFBFanpage = """
                select * from fbfanpage_lastpost f where f.post_message like %s or f.post_message like %s
            """

            # 重置新聞在各平台的討論次數
            news_ptt_message_all_count: int = 0
            news_fbfanpage_message_all_count: int = 0

            print(index, lendfNewsList)
            # 取得ptt有該則新聞的清單
            dfNewsInPtt = pd.read_sql(
                sql=queryNewsInPtt,
                con=conn,
                params=("%" + dfNewsRow["title"] + "%", "%" + dfNewsRow["url"] + "%"),
            )  # mysql query
            if not dfNewsInPtt.empty:
                print(dfNewsRow["newsuuid"], dfNewsRow["title"], dfNewsRow["url"])

                # 如果該新聞出現在ptt則加總其留言量
                # 按規劃，臉書的情緒加權20，留言加權未設定
                for index, dfNewsInPttRow in dfNewsInPtt.iterrows():
                    print(
                        dfNewsInPttRow["article_id"],
                        dfNewsInPttRow["message_count.all"],
                        dfNewsInPttRow["triger_time"],
                    )
                    news_ptt_message_all_count = (
                        news_ptt_message_all_count
                        + int(dfNewsInPttRow["message_count.all"]) * 20
                    )

                print(
                    "news_ptt_message_all_count: {}".format(news_ptt_message_all_count)
                )

            # 取得fbfanpage有該則新聞的清單
            dfNewsInFBFanpage = pd.read_sql(
                sql=queryNewsInFBFanpage,
                con=conn,
                params=("%" + dfNewsRow["title"] + "%", "%" + dfNewsRow["url"] + "%"),
            )  # mysql query
            if not dfNewsInFBFanpage.empty:
                print(dfNewsRow["newsuuid"], dfNewsRow["title"], dfNewsRow["url"])

                # 如果該新聞出現在粉絲頁則加總其留言量
                # 按規劃，臉書的情緒加權10，留言加權50
                for index, dfNewsInFBFanpageRow in dfNewsInFBFanpage.iterrows():
                    print(
                        dfNewsInFBFanpageRow["sys_id"],
                        dfNewsInFBFanpageRow["post_comment_count"],
                        dfNewsInFBFanpageRow["allEmoji"],
                        dfNewsInFBFanpageRow["crawler_time"],
                    )
                    news_fbfanpage_message_all_count = (
                        news_fbfanpage_message_all_count
                        + int(dfNewsInFBFanpageRow["post_comment_count"]) * 50
                        + int(dfNewsInFBFanpageRow["allEmoji"]) * 10
                    )

                print(
                    "news_fbfanpage_message_all_count: {}".format(
                        news_fbfanpage_message_all_count
                    )
                )

            # 加總現在的聲量
            volume_now = int(news_ptt_message_all_count) + int(
                news_fbfanpage_message_all_count
            )
            if volume_now > 0:
                newsVolume["newsuuid"].append(dfNewsRow["newsuuid"])
                newsVolume["volume_now"].append(volume_now)
                newsVolume["ptt_volume"].append(int(news_ptt_message_all_count))
                newsVolume["fb_fanpage_volume"].append(
                    int(news_fbfanpage_message_all_count)
                )

        df = pd.DataFrame.from_dict(newsVolume)
        print(df)

        df.to_sql(DBSRV_VOLUME_TABLE, con=engine, if_exists="append", index=False)

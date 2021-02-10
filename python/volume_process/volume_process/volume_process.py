# -*-coding:utf-8 -*-

# read as csv
import pandas as pd
from sqlalchemy import create_engine
from dynaconf import settings
from datetime import datetime

# 從setting.toml中讀取資料庫相關設定
DBSRV_IP = settings.DBSRV_IP
DBSRV_PORT = settings.DBSRV_PORT
DBSRV_USERNAME = settings.DBSRV_USERNAME
DBSRV_PASSWORD = settings.DBSRV_PASSWORD
DBSRV_SCHEMA = settings.DBSRV_SCHEMA
DBSRV_VOLUME_TABLE = settings.DBSRV_VOLUME_TABLE
DBSRV_BOMB_TABLE = settings.DBSRV_BOMB_TABLE


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
                        + int(dfNewsInPttRow["message_count.push"]) * 200
                        + int(dfNewsInPttRow["message_count.boo"]) * 200
                        + int(dfNewsInPttRow["message_count.neutral"]) * 50
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

    def calculate_bomb(self):
        # 利用聲量來做為爆發力的計算基準

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

        # 檢索最新的聲量
        queryVolumeList = "select * from volume_last vl "

        # 取得生量清單
        dfVolume = pd.read_sql(sql=queryVolumeList, con=conn)  # mysql query
        lendfVolume: int = len(dfVolume)

        # 用來儲存 bomb 的斜率
        newsBomb: dict = {
            "newsuuid": [],
            "bomb_now": [],
        }

        # print(generator_df)
        for index, dfVolumeRow in dfVolume.iterrows():

            # 檢查該聲量的全部歷程
            queryVolume = """
                select * from volume v where v.newsuuid = %s order by v.calculate_time
            """

            print(index, lendfVolume, dfVolumeRow["newsuuid"])
            # 取得新聞的聲量歷程
            dfVolumeInVolumes = pd.read_sql(
                sql=queryVolume,
                con=conn,
                params=(dfVolumeRow["newsuuid"],),
            )  # mysql query
            if not dfVolumeInVolumes.empty:
                # print(dfVolumeRow["newsuuid"], dfVolumeRow["volume_now"])

                # 爆發力公式
                # 爆發力 ＝ 現在聲量 / 新聞出現至今秒數（現在timestamp - 第一次出現的時間timestamp）
                for index, dfVolumeInVolumesRow in dfVolumeInVolumes.iterrows():
                    # print(
                    #     index,
                    #     dfVolumeInVolumesRow["newsuuid"],
                    #     dfVolumeInVolumesRow["volume_now"],
                    #     dfVolumeInVolumesRow["calculate_time"],
                    #     str(dfVolumeInVolumesRow["calculate_time"]),
                    # )

                    first_date: str = str(dfVolumeInVolumesRow["calculate_time"])
                    bomb_now: float = 0

                    # 只對最早的一筆聲量時間進行比較，用該新文第一次出現聲量的時間，
                    # 來做為 X0 的值
                    if index == 0:

                        # 取得該新聞第一次出現至今的秒數
                        timediff = (
                            datetime.now()
                            - datetime.strptime(first_date, "%Y-%m-%d %H:%M:%S")
                        ).seconds

                        if timediff > 0:
                            # print(f'now volume: {dfVolumeRow["volume_now"]}')
                            # print(f'last volume: {dfVolumeInVolumesRow["volume_now"]}')
                            bomb_now = (
                                int(dfVolumeInVolumesRow["volume_now"]) / timediff
                            )
                            print(
                                f"time diff: {timediff},volumenow: {dfVolumeInVolumesRow['volume_now']}, bomb_now: {bomb_now}"
                            )

                            if bomb_now > 0:
                                newsBomb["newsuuid"].append(
                                    dfVolumeInVolumesRow["newsuuid"]
                                )
                                newsBomb["bomb_now"].append(bomb_now)

                        break

        df = pd.DataFrame.from_dict(newsBomb)
        print(df)

        df.to_sql(DBSRV_BOMB_TABLE, con=engine, if_exists="append", index=False)

    def replace_old_vwNews(self):
        # 將計算後的結果，原本以view表呈現，
        # 但這樣太耗計算資源，因此將view表直接轉成一般table
        # 很粗暴，不過目前先這樣，如果後續有時間再調整

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

        print("建立 Temp_vwNews 暫存表")
        # 先將view表讀出來，建立暫存表，再清掉舊的，再把名字改成新的
        creatTemp_vwNewsVolumeList = """ create table Temp_vwNews as \
                                            select * from vwNews_view vn  """
        conn.execute(creatTemp_vwNewsVolumeList)

        print("移除 old vwNews 表")
        # 先將view表讀出來，建立暫存表，再清掉舊的，再把名字改成新的
        drop_vwNews = """ DROP TABLE vwNews; """
        conn.execute(drop_vwNews)

        print("將 Temp_vwNews 改名為 vwNews_view")
        # 先將view表讀出來，建立暫存表，再清掉舊的，再把名字改成新的
        rename_Temp_vwNews = """ RENAME TABLE Temp_vwNews TO vwNews; """
        conn.execute(rename_Temp_vwNews)
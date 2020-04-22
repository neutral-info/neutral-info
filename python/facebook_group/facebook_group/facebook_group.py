from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
from datetime import timedelta, date
import json
from dynaconf import settings
from PIL import Image
import pytesseract


class FacebookGroupCrawler(object):
    # 從setting.toml中讀取臉書帳密
    username = settings.FBUSERNAME
    password = settings.FBUSERPASSWORD

    fbposts: dict = {}
    fbgroup = ""
    data_path = ""

    chrome_options = Options()
    if settings.HEADLESS != "":
        chrome_options.add_argument(settings.HEADLESS)  # 啟動無頭模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://www.facebook.com")
    time.sleep(3)

    def __init__(self, cmdline=None, as_lib=False):

        print("1.1 登入臉書")
        element_login_username = (By.ID, "email")
        element_login_password = (By.ID, "pass")
        element_login_button = (By.ID, "loginbutton")
        self.driver.find_element(*element_login_username).send_keys(self.username)
        self.driver.find_element(*element_login_password).send_keys(self.password)
        self.driver.find_element(*element_login_button).click()
        time.sleep(3)

    def start_Crawler(self, fbgroup, data_path):
        # 取得執行爬取的社團
        self.fbgroup = fbgroup

        # 取的資料下載的路徑
        self.data_path = data_path

        # 取得往下捲12次後在『動態消息』的貼文
        htmltext = self.get_htmltext(self.username, self.password)

        # 解析發文時間是近一個禮拜的貼文內容
        # todo: 是否要調整時間的定義？
        startdate = datetime.datetime.combine(
            date.today() + timedelta(days=-7), datetime.datetime.min.time()
        )
        enddate = datetime.datetime.combine(
            date.today() + timedelta(days=1), datetime.datetime.min.time()
        )
        print("0.1 抓取 {} 到 {} 的貼文".format(startdate, enddate))
        self.parse_htmltext(htmltext, startdate, enddate)

        # 解析單篇貼文中的情緒
        self.parse_post(self.username, self.password)

        # 將抓到的整個貼文資料寫成一個JSON檔
        fbpostjsonfilename = self.data_path + "/fbGroupPost_{}_{}.log".format(
            fbgroup, datetime.datetime.now().timestamp()
        )
        print("0.2 將貼文資料寫入:{}".format(fbpostjsonfilename))
        with open(fbpostjsonfilename, "w", encoding="utf8") as f:
            json.dump(self.fbposts, f, ensure_ascii=False)

    def get_htmltext(self, username, password):
        """
        取得特定社團往下捲12次後的HTML全文
        """

        print("1.2 切換到特定社團", self.fbgroup)
        self.driver.get("https://www.facebook.com/groups/" + self.fbgroup + "/")
        time.sleep(3)

        # 往下捲12次
        print("1.3 預計往下捲12次")
        for i in range(12):
            if i > 0:
                time.sleep(2)
            y = 4000 * (i + 1)
            self.driver.execute_script(f"window.scrollTo(0, {y})")
            print(
                "1.3 往下捲第 {} 次".format(i), end="\r",
            )

        htmltext = self.driver.page_source
        print("1.4 已取得往下捲12次後在『動態消息』的貼文")

        return htmltext

    def parse_htmltext(self, htmltext, start_date, end_date):
        """
        解析臉書貼文與回覆的原始碼。

        htmltext:  為原始碼，str
        star_date: 為起始日期，datetime.datetime
        end_date:  為結束日期，datetime.datetime
        """
        post_ids = []
        post_persons = []
        post_messages = []
        post_times = []
        ustart_date = start_date.timestamp()
        uend_date = end_date.timestamp()
        soup = BeautifulSoup(htmltext, "html.parser")
        body = soup.find("body")
        posts = body.select('div[id="pagelet_group_mall"]')[0].select(
            'div[aria-label="動態消息"]'
        )[0]
        feed_articles = posts.select('div[role="feed"]')[0].select(
            'div[role="article"]'
        )
        other_articles = posts.select('div[role="article"]')

        # 蒐集全部貼文
        articles = feed_articles + other_articles
        # articles = other_articles

        for article in articles:
            # 貼文相關資料
            if article.has_attr("id"):
                try:
                    post_person = (
                        re.findall('ajaxify="(.*?)"', str(article))[0]
                        .split("&")[1]
                        .split("member_id=")[1]
                    )
                except Exception:
                    continue
                post_time = int(re.findall('data-utime="(.*?)"', str(article))[0])
                post_id = re.findall('id="mall_post_(.*?):6:0"', str(article))[0]
                # 如果是轉貼文，它的ID表示法有所不同
                if len(post_id) > 20:
                    post_id = post_id.split(";")[2]

                # 取得貼文內文
                post_msg = article.select('div[data-testid="post_message"]')
                if len(post_msg) > 0:
                    post_message = post_msg[0].get_text()
                else:
                    post_message = "Sticker"

                # 檢查貼文間區間是否符合目標
                if post_time >= ustart_date and post_time <= uend_date:
                    post_ids.append(post_id)
                    post_times.append(post_time)
                    post_persons.append(post_person)
                    post_messages.append(post_message)

                try:
                    # 貼文基本JSON物件
                    postjson = {}
                    postjson.setdefault(
                        post_id,
                        {
                            "sys_id": "facebookgroup_" + self.fbgroup + "_" + post_id,
                            "sys_type": "facebookgroup",
                            "board_id": self.fbgroup,
                            "post_id": post_id,
                            "post_time": post_time,
                            "post_person": post_person,
                            "post_message": post_message,
                        },
                    )
                    self.fbposts.update(postjson)
                except Exception:
                    pass
        print("2.1 已解析『動態消息』近一個禮拜的貼文狀態")

    def parse_post(self, username, password):
        """
        抓取特定貼文的使用者態度
        採用的方法是，把每一個貼文的固定網址打開後點選對應的情緒列後分析

        username 你的臉書帳號
        password 你的臉書密碼

        """

        postcount = 0
        for post_id in self.fbposts.keys():
            postcount += 1
            print(
                "3.1 {}/{} 貼文ID: {}".format(postcount, len(self.fbposts), post_id),
                end="\r",
            )
            self.driver.get(
                "http://www.facebook.com/groups/"
                + self.fbgroup
                + "/permalink/"
                + post_id
            )

            # 如果貼文沒有文字內容，就嘗試取得貼文照片
            if self.fbposts[post_id]["post_message"] == "Sticker":
                soupArticle = BeautifulSoup(self.driver.page_source, "html.parser")
                postScaledImage = soupArticle.select('div[role="article"]')[0].select(
                    'img[class="scaledImageFitWidth img"]'
                )
                postImg = re.findall('src="(.*?)"', str(postScaledImage))
                if len(postImg) > 1:
                    postImgUrl = postImg[0].replace("amp;", "")
                    try:
                        requestImage = requests.get(postImgUrl, allow_redirects=True)
                        open("temp.jpg", "wb").write(requestImage.content)
                        # OCR圖片取得其中的文字
                        img = Image.open("temp.jpg")
                        ocrText = pytesseract.image_to_string(
                            img,
                            lang="chi_tra",
                            config=settings.TESSDATA_DIR_CONFIG,
                            nice=0,
                            timeout=0,
                        )
                        self.fbposts[post_id]["post_message"] = ocrText
                    except Exception as e:
                        print(
                            "\nload {} post image fail: {}".format(post_id, e.args[0])
                        )
                        time.sleep(2)

            # 建立一個函式用於檢測是否有『更多留言』或『檢視另XX則留言』出現
            def checkMoreComment():
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[@class="_4swz _293g"]')
                        )
                    )
                    time.sleep(1)
                    while True:
                        try:
                            element_morecomment = (
                                By.XPATH,
                                '//div[@class="_4swz _293g"]',
                            )
                            self.driver.find_element(*element_morecomment).click()
                        except Exception as e:
                            # 直到找不到comment的連結才跳出
                            print(
                                "\nclick {} expand comment fail: {}".format(
                                    post_id, e.args[0]
                                )
                            )
                            time.sleep(2)
                            break
                        else:
                            checkMoreComment()
                            break
                except Exception as e:
                    print("\n{} no expand comment link: {}".format(post_id, e.args[0]))
                    time.sleep(2)

            checkMoreComment()

            # 建立一個函式用於檢測是否留言中是否還有回留言『XX則回覆』出現
            def checkMoreReplyComment():
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//span[@class="_4sso _4ssp"]')
                        )
                    )
                    time.sleep(1)
                    while True:
                        try:
                            element_morereplycomment = (
                                By.XPATH,
                                '//span[@class="_4sso _4ssp"]',
                            )
                            self.driver.find_element(*element_morereplycomment).click()
                        except Exception as e:
                            print(
                                "\nclick {} reply comment fail: {}".format(
                                    post_id, e.args[0]
                                )
                            )
                            time.sleep(2)
                            break
                        else:
                            checkMoreReplyComment()
                            break
                except Exception as e:
                    print("\n{} no reply comment link: {}".format(post_id, e.args[0]))
                    time.sleep(2)

            checkMoreReplyComment()

            # 讀取回文內容
            soupSomeArticle = BeautifulSoup(self.driver.page_source, "html.parser")
            postComment = []
            try:
                # aria-label="留言"
                listComments = soupSomeArticle.findAll("div", {"aria-label": "留言"})
                for listComment in listComments:
                    try:
                        CommentUserID = re.findall(
                            'data-hovercard="(.*?)"', str(listComment)
                        )[0].split("id=")[1]
                    except Exception:
                        CommentUserID = "error"

                    try:
                        CommentContent = listComment.find("span", {"dir": "ltr"}).text
                    except Exception:
                        CommentContent = "Sticker"

                    try:
                        CommentTimestamp = re.findall(
                            'data-utime="(.*?)"', str(listComment)
                        )[0]
                    except Exception:
                        CommentTimestamp = "error"

                    # 建立回文物件
                    postCommentContent = {
                        "comment_person": CommentUserID,
                        "comment_message": CommentContent,
                        "comment_time": CommentTimestamp,
                    }
                    postComment.append(postCommentContent)

                self.fbposts[post_id].update({"postComment": postComment})

            except Exception as e:
                print("\n{} read comment fail: {}".format(post_id, e.args[0]))
                time.sleep(2)

            try:
                # 等待情緒列的出現，出現後則點選
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//a[@data-testid="UFI2ReactionsCount/root"]')
                    )
                )
                while True:
                    try:
                        # 因應往下捲蒐集回應的動作，導致偵測情緒列會失敗的狀況，所以先捲回到畫面最前頭，避免等下FIND不到
                        self.driver.execute_script(f"window.scrollTo(0, 0)")
                        element_emoji = (
                            By.XPATH,
                            '//a[@data-testid="UFI2ReactionsCount/root"]',
                        )
                        self.driver.find_element(*element_emoji).click()
                    except Exception as e:
                        print("\n{} click emoji tab fail,{}".format(post_id, e.args[0]))
                        time.sleep(2)
                        continue
                    else:
                        break
            except Exception as e:
                print("\n{} no emoji tab link: {}".format(post_id, e.args[0]))
                time.sleep(2)

            try:
                # 確認popup已經出現後才讀取情緒
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="_21ab"]'))
                )
                time.sleep(1)
                while True:
                    try:
                        soupPopupEmoji = BeautifulSoup(
                            self.driver.page_source, "html.parser"
                        )
                        # Emoji tab
                        soupEmojiTab = soupPopupEmoji.find("div", {"class": "_21ab"})
                    except Exception as e:
                        print(
                            "\n{} click emoji popup fail,{}".format(post_id, e.args[0])
                        )
                        time.sleep(2)
                        continue
                    else:
                        break
            except Exception as e:
                print("\n{} no emoji popup: {}".format(post_id, e.args[0]))
                time.sleep(2)

            allEmoji = 0
            goodEmoji = 0
            haEmoji = 0
            waEmoji = 0
            heartEmoji = 0
            angryEmoji = 0
            cryEmoji = 0

            # 拆解情緒列的內容及對應的次數
            try:
                listEmoji = re.findall('aria-label="(.*?)"', str(soupEmojiTab))
                for emojistring in listEmoji:
                    emojitype = emojistring.split(" ")[1]
                    emojicount = int(emojistring.split(" ")[0].replace(",", ""))
                    # print('emojistring', emojistring)
                    if emojitype == "人對這則貼文傳達了心情":
                        allEmoji = emojicount
                    elif emojitype == "人表示讚":
                        goodEmoji = emojicount
                    elif emojitype == "人表示哈":
                        haEmoji = emojicount
                    elif emojitype == "人表示哇":
                        waEmoji = emojicount
                    elif emojitype == "人表示大心":
                        heartEmoji = emojicount
                    elif emojitype == "人用怒傳達了心情":
                        angryEmoji = emojicount
                    elif emojitype == "人表示嗚":
                        cryEmoji = emojicount
            except Exception as e:
                print("\n{} no emoji count: {}".format(post_id, e.args[0]))
                time.sleep(2)

            # 產生貼文情緒的JSON物件，並回寫
            emojiDict = {}
            emojiDict.setdefault(
                "emoji",
                {
                    "allEmoji": allEmoji,
                    "goodEmoji": goodEmoji,
                    "haEmoji": haEmoji,
                    "waEmoji": waEmoji,
                    "heartEmoji": heartEmoji,
                    "angryEmoji": angryEmoji,
                    "cryEmoji": cryEmoji,
                },
            )

            self.fbposts[post_id].update(emojiDict)


if __name__ == "__main__":
    """
    程式參考：
    1. https://freelancerlife.info/zh/blog/python%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2%E6%87%89%E7%94%A8-facebook%E7%A4%BE%E5%9C%98%E6%88%90%E5%93%A1%E5%8F%83%E8%88%87%E5%BA%A6%E5%88%86%E6%9E%90/
    2. 一位伙伴茹的CODE

    功能說明：
    1. 進到特定的臉書社團後，會將該社團的動態消息往下捲12次
    2. 蒐集動態消息中的貼文時間是近七天的
    3. 蒐集貼文主體的情緒狀態
    4. 蒐集貼文回文的內容
    5. 產生一個JSON存放資料，檔名格式：fbGroupPost_{group id}_{bot finish timestamp}.json

    todo:
    1. 社團採外部序號導入自動迴圈執行
    2. 貼文內容是圖片時要怎處理？直接解圖？下載存放就好？（放在哪？怎傳遞？）

    程式說明：
    1. 請先修改帳密，密碼檔請參考settings_sample.toml檔案，修改後另存為settings.toml
    2. 確認webdriver路徑

    臉書環境：
    1. 此bot請在台灣繁體中文環境執行
    2. 建議先手動登入確認該臉書帳號，是否會跳出任何其它要求確認的畫面，
       如有先將關閉，避免程式誤判

    """
    c = FacebookGroupCrawler()

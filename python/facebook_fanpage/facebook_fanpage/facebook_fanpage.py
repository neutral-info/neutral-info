from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import re
import datetime
from datetime import timedelta, date
import json
from time import sleep
from dynaconf import settings
from PIL import Image
import pytesseract


class FacebookFanpageCrawler(object):
    # 給後面初始化webdriver使用
    driver = None

    # 從setting.toml中讀取臉書帳密
    username = settings.FBUSERNAME
    password = settings.FBUSERPASSWORD

    fbposts: dict = {}
    fbfanpage = ""
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

    def start_Crawler(self, fbfanpage, data_path):
        # 帶入相關參數
        self.fbposts = {}
        self.fbfanpage = fbfanpage
        self.data_path = data_path

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("http://www.facebook.com")
        sleep(3)

        print("1.1 登入臉書")
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            sleep(1)
            while True:
                try:
                    element_login_username = (By.ID, "email")
                    element_login_password = (By.ID, "pass")
                    element_login_button = (By.ID, "loginbutton")
                    self.driver.find_element(*element_login_username).send_keys(
                        self.username
                    )
                    self.driver.find_element(*element_login_password).send_keys(
                        self.password
                    )
                    self.driver.find_element(*element_login_button).click()
                    sleep(3)
                except Exception as e:
                    # 直到找不到comment的連結才跳出
                    print("\nlogin facebook fail: {}".format(e.args[0]))
                    sleep(2)
                    break
                else:
                    break
        except Exception as e:
            print("\nCan't find login's email: {}".format(e.args[0]))
            sleep(2)

        # 取得執行爬取的粉絲頁
        self.fbfanpage = fbfanpage

        # 取的資料下載的路徑
        self.data_path = data_path

        # 取得往下捲12次後在『動態消息』的貼文
        htmltext = self.get_htmltext(self.username, self.password)

        # 解析發文時間是近一個禮拜的貼文內容
        # todo: 是否要調整時間的定義？
        startdate = datetime.datetime.combine(
            date.today() + timedelta(days=-1), datetime.datetime.min.time()
        )
        enddate = datetime.datetime.combine(
            date.today() + timedelta(days=1), datetime.datetime.min.time()
        )
        print("0.1 抓取 {} 到 {} 的貼文".format(startdate, enddate))
        self.parse_htmltext(htmltext, startdate, enddate)

        # 解析單篇貼文中的情緒
        self.parse_post(self.username, self.password)

        # 將抓到的整個貼文資料寫成一個JSON檔
        fbpostjsonfilename = self.data_path + "/fbFanpagePost_{}_{}.log".format(
            fbfanpage, datetime.datetime.now().timestamp()
        )
        print("0.2 將貼文資料寫入:{}".format(fbpostjsonfilename))
        with open(fbpostjsonfilename, "w", encoding="utf8") as f:
            # 調整成特殊JSON格式供filebeat使用
            if self.fbposts:  # a check to determine that our array is not empty
                for (
                    fbpost
                ) in self.fbposts.values():  # now loop through your elements one by one
                    json.dump(
                        fbpost, f, ensure_ascii=False
                    )  # JSON encode each element and write it to the file
                    f.write(
                        ",\n"
                    )  # close the element entry with a comma and a new line
                # f.seek(-3, 1)  # go back to the last separator to clear out the comma
            f.truncate()

        # 關掉webdriver降低記憶體使用量
        self.driver.quit()
        print("0.3 close webdriver")

    def get_htmltext(self, username, password):
        """
        取得特定社團往下捲12次後的HTML全文
        """

        print("1.2 切換到特定粉絲團", self.fbfanpage)
        self.driver.get("https://www.facebook.com/pg/" + self.fbfanpage + "/posts")
        sleep(3)

        # 往下捲12次
        print("1.3 預計往下捲12次")
        for i in range(12):
            y = 4000 * (i + 1)
            self.driver.execute_script(f"window.scrollTo(0, {y})")
            print(
                "1.3 往下捲第 {} 次".format(i), end="\r",
            )
            sleep(2)

        # 建立一個函式用於檢測是否有貼文內容是否都已展開，如還有『更多』就點一下
        def checkMoreContent():
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//a[@class="see_more_link"]')
                    )
                )
                sleep(1)
                while True:
                    try:
                        element_morecontentlink = (
                            By.XPATH,
                            '//div[@class="_5pbx userContent _3576"]//span[@class="text_exposed_link"]',
                        )
                        find_morecontentlinks = self.driver.find_elements(
                            *element_morecontentlink
                        )
                        # 將貼文內容本身帶有『更多』的連結都點一下
                        for find_morecontentlink in find_morecontentlinks:
                            actions = ActionChains(self.driver)
                            actions.move_to_element(find_morecontentlink).perform()
                            actions.click(find_morecontentlink).perform()
                            print(
                                "click {} expand content more link!".format(
                                    self.fbfanpage
                                ),
                                end="\r",
                            )
                    except Exception as e:
                        # 直到找不到content的連結才跳出
                        print(
                            "\nclick {} expand content fail: {}".format(
                                self.fbfanpage, e.args[0]
                            )
                        )
                        sleep(2)
                        break
                    else:
                        print(
                            "finish click {} expand content more link!".format(
                                self.fbfanpage
                            )
                        )
                        break
            except Exception as e:
                print(
                    "\n{} no expand content link: {}".format(self.fbfanpage, e.args[0])
                )
                sleep(2)

        checkMoreContent()

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

        # 抓取使用者貼文的主要區域
        articles = body.select('div[class="_5pcr userContentWrapper"]')

        for article in articles:
            # 因為粉絲頁的作者就是粉絲頁本人，所以就是粉絲頁的對應帳號
            post_person = self.fbfanpage

            # 找出貼文的id
            try:
                post_id = article.select("div[data-testid='story-subtitle']")[0]
                post_id = re.findall(' id="(.*?)"', str(post_id))[0].split(";")[1]
                # print("post_id", post_id)
            except Exception as e:
                print("\n get post_id error:{}".format(e.args[0]))
                pass

            # 取得系統標示貼文的時間
            post_time = int(re.findall('data-utime="(.*?)"', str(article))[0])

            # 取得貼文內文
            try:
                post_msg = article.select('div[data-testid="post_message"]')
                if len(post_msg) > 0:
                    post_message = post_msg[0].get_text()
                else:
                    post_message = "Sticker"
                # print("post_message", post_message)
            except Exception as e:
                print("\n get post_msg error:{}".format(e.args[0]))
                pass

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
                            "sys_id": "facebookfanpage_"
                            + self.fbfanpage
                            + "_"
                            + post_id,
                            "sys_type": "facebookfanpage",
                            "board_id": self.fbfanpage,
                            "post_id": post_id,
                            "post_time": post_time,
                            "post_person": post_person,
                            "post_message": post_message,
                        },
                    )
                    self.fbposts.update(postjson)
                except Exception:
                    pass
        print("2.1 已解析『動態消息』近一個禮拜的貼文狀態，計有 {} 筆".format(len(self.fbposts)))

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
                # end="\r",
            )
            self.driver.get(
                "http://www.facebook.com/" + self.fbfanpage + "/posts/" + post_id
            )

            # 等待貼文跳出來的畫面，之後才關閉
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//a[@class="_xlt _418x"]')
                    )
                )
                sleep(1)
                while True:
                    try:
                        element_morecomment = (
                            By.XPATH,
                            '//a[@class="_xlt _418x"]',
                        )
                        self.driver.find_element(*element_morecomment).click()
                    except Exception as e:
                        # 一直到找不到可以取消的連結就跳出
                        print(
                            "\nclick {} close post popup fail: {}".format(
                                post_id, e.args[0]
                            )
                        )
                        sleep(2)
                        break
            except Exception as e:
                print("\n{} no close post popup link: {}".format(post_id, e.args[0]))
                sleep(2)
                pass

            # 如果貼文沒有文字內容，就嘗試取得貼文照片
            if self.fbposts[post_id]["post_message"] == "Sticker":
                soupArticle = BeautifulSoup(self.driver.page_source, "html.parser")
                try:
                    postScaledImage = soupArticle.select('div[role="article"]')[
                        0
                    ].select('img[class="scaledImageFitWidth img"]')
                    postImg = re.findall('src="(.*?)"', str(postScaledImage))
                except Exception as e:
                    print(
                        "\n{} post is sticker without image: {}".format(
                            post_id, e.args[0]
                        )
                    )
                    postImg = []
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
                        sleep(2)

            # 建立一個函式用於檢測是否有『更多留言』或『檢視另XX則留言』出現
            def checkMoreComment():
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@class="permalinkPost"]//a[@class="_4sxc _42ft"]',
                            )
                        )
                    )
                    sleep(1)
                    while True:
                        try:
                            element_morecomment = (
                                By.XPATH,
                                '//div[@class="permalinkPost"]//a[@class="_4sxc _42ft"]',
                            )
                            self.driver.find_element(*element_morecomment).click()
                            print(
                                "3.1.1 {}/{} 貼文ID: {}, action:checkMoreComment".format(
                                    postcount, len(self.fbposts), post_id
                                ),
                                end="\r",
                            )
                        except Exception as e:
                            # 直到找不到comment的連結才跳出
                            print(
                                "\nclick {} expand comment fail: {}".format(
                                    post_id, e.args[0]
                                )
                            )
                            sleep(2)
                            break
                        else:
                            checkMoreComment()
                            break
                except Exception as e:
                    print("\n{} no expand comment link: {}".format(post_id, e.args[0]))
                    sleep(2)

            checkMoreComment()

            # 建立一個函式用於檢測是否留言中是否還有回留言『XX則回覆』出現
            def checkMoreReplyComment():
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//div[@class="permalinkPost"]//a[@class="_4sxc _42ft"]',
                            )
                        )
                    )
                    sleep(1)
                    while True:
                        try:
                            element_morereplycomment = (
                                By.XPATH,
                                '//div[@class="permalinkPost"][contains(@class, "_4sxc _42ft"]',
                            )
                            self.driver.find_element(*element_morereplycomment).click()
                            print(
                                "3.1.2 {}/{} 貼文ID: {}, action:checkMoreReplyComment".format(
                                    postcount, len(self.fbposts), post_id
                                ),
                                end="\r",
                            )
                        except Exception as e:
                            print(
                                "\nclick {} reply comment fail: {}".format(
                                    post_id, e.args[0]
                                )
                            )
                            sleep(2)
                            break
                        else:
                            checkMoreReplyComment()
                            break
                except Exception as e:
                    print("\n{} no reply comment link: {}".format(post_id, e.args[0]))
                    sleep(2)

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
                sleep(2)

            try:
                # 等待情緒列的出現，出現後則點選
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//div[@class="permalinkPost"]//a[@data-testid="UFI2ReactionsCount/root"]',
                        )
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
                        print(
                            "3.1.3 {}/{} 貼文ID: {}, action:clickEmojiTab".format(
                                postcount, len(self.fbposts), post_id
                            ),
                            end="\r",
                        )
                    except Exception as e:
                        print("\n{} click emoji tab fail,{}".format(post_id, e.args[0]))
                        sleep(2)
                        break
                    else:
                        break
            except Exception as e:
                print("\n{} no emoji tab link: {}".format(post_id, e.args[0]))
                sleep(2)

            try:
                # 確認popup已經出現後才讀取情緒
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="_21ab"]'))
                )
                sleep(1)
                while True:
                    try:
                        soupPopupEmoji = BeautifulSoup(
                            self.driver.page_source, "html.parser"
                        )
                        # Emoji tab
                        soupEmojiTab = soupPopupEmoji.find("div", {"class": "_21ab"})
                        print(
                            "3.1.4 {}/{} 貼文ID: {}, action:getEmojiTab".format(
                                postcount, len(self.fbposts), post_id
                            ),
                            end="\r",
                        )
                    except Exception as e:
                        print("\n{} emoji popup fail,{}".format(post_id, e.args[0]))
                        sleep(2)
                        continue
                    else:
                        break
            except Exception as e:
                print("\n{} no emoji popup: {}".format(post_id, e.args[0]))
                sleep(2)

            allEmoji: int = 0
            goodEmoji: int = 0
            haEmoji: int = 0
            waEmoji: int = 0
            heartEmoji: int = 0
            angryEmoji: int = 0
            cryEmoji: int = 0
            comeonEmoji: int = 0

            # 拆解情緒列的內容及對應的次數
            # todo:如果太多情緒類型，會多一個更多要處理，目前先不處理，等之後有時間再處理
            try:
                listEmoji = re.findall('aria-label="(.*?)"', str(soupEmojiTab))
                for emojistring in listEmoji:
                    emojitype = str(emojistring).split()
                    # 如果個別情緒數量超過一萬，需特別處理
                    if emojitype[1].find("萬") == 0:
                        emojitype[1] = emojitype[1].replace("萬", "")
                        emojicount = int(
                            float(str(emojistring).split()[0].replace(",", "")) * 10000
                        )
                    else:
                        emojicount = int(str(emojistring).split()[0].replace(",", ""))

                    # 針對其標籤判斷屬於何種情緒
                    if emojitype[1] == "人對這則貼文傳達了心情":
                        allEmoji = emojicount
                    elif emojitype[1] == "人表示讚":
                        goodEmoji = emojicount
                    elif emojitype[1] == "人表示哈":
                        haEmoji = emojicount
                    elif emojitype[1] == "人表示哇":
                        waEmoji = emojicount
                    elif emojitype[1] == "人表示大心":
                        heartEmoji = emojicount
                    elif emojitype[1] == "人表示怒":
                        angryEmoji = emojicount
                    elif emojitype[1] == "人表示嗚":
                        cryEmoji = emojicount
                    elif emojitype[1] == "人表示加油":
                        comeonEmoji = emojicount
            except Exception as e:
                print("\n{} no emoji count: {}".format(post_id, e.args[0]))
                sleep(2)

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
                    "comeonEmoji": comeonEmoji,
                },
            )
            print("\nemojiDict", emojiDict)

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
    c = FacebookFanpageCrawler()

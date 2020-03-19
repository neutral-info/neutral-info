from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import datetime


def get_htmltext(username, password):
    '''
    取得特定社團的貼文

    username 你的臉書帳號
    password 你的臉書密碼
    '''
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path='./geckodriver')
    driver.get("http://www.facebook.com")
    time.sleep(3)
    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("loginbutton").click()
    time.sleep(3)
    driver.get('https://www.facebook.com/groups/733787316774129/')
    time.sleep(3)
    for i in range(12):
        y = 4000 * (i + 1)
        driver.execute_script(f"window.scrollTo(0, {y})")
        time.sleep(2)

    def ClickForMore():
        hrefBtns = driver.find_elements_by_tag_name('a')
        for btn in hrefBtns:
            try:
                s = btn.get_attribute('data-testid')
            except:
                continue
            if s == 'UFI2CommentsPagerRenderer/pager_depth_1' or s == 'UFI2CommentsPagerRenderer/pager_depth_0':
                try:
                    btn.click()
                    time.sleep(1)
                except:
                    continue

    ClickForMore()
    ClickForMore()

    htmltext = driver.page_source
    driver.close()

    return htmltext


def parse_htmltext(htmltext, start_date, end_date):
    '''
    解析臉書貼文與回覆的原始碼。
    htmltext為原始碼，str
    star_date為起始日期，datetime.datetime
    end_date為結束日期，datetime.datetime
    '''
    post_persons = []
    comment_persons = []
    good_urllist = []
    ustart_date = start_date.timestamp()
    uend_date = end_date.timestamp()
    soup = BeautifulSoup(htmltext, 'html.parser')
    body = soup.find('body')
    posts = body.select('div[id="pagelet_group_mall"]')[
        0].select('div[aria-label="動態消息"]')[0]
    feed_articles = posts.select('div[role="feed"]')[
        0].select('div[role="article"]')
    other_articles = posts.select('div[role="article"]')
    articles = feed_articles + other_articles

    for article in articles:
        if article.has_attr('id'):
            try:
                post_person = re.findall(
                    'title="(.{2,20})"><div class=', str(article))[0]
            except:
                continue
            post_time = int(re.findall('data-utime="(.*?)"', str(article))[0])
            if post_time >= ustart_date and post_time <= uend_date:
                post_persons.append(post_person)
            try:
                good_urllist.append(re.findall(
                    '"(/ufi/reaction/profile/browser/\?.*?)"', str(article))[0])
            except:
                pass

        elif article.has_attr('data-testid'):
            comment_person = re.findall(
                'directed_target_id.*?href=".*?">(.*?)</a>', str(article))[0]
            comment_time = int(re.findall(
                'data-utime="(.*?)"', str(article))[0])
            if comment_time >= ustart_date and post_time <= uend_date:
                comment_persons.append(comment_person)
                try:
                    good_urllist.append(re.findall(
                        '"(/ufi/reaction/profile/browser/\?.*?)"', str(article))[0])
                except:
                    pass

    return post_persons, comment_persons, good_urllist

def parse_good_urllist(username, password, urllist):
    '''
    抓取特定貼文的使用者態度

    username 你的臉書帳號
    password 你的臉書密碼
    
    '''

    output = []

    profile = webdriver.FirefoxProfile()
    # Finally, turned off webnotifications...
    profile.set_preference("dom.webnotifications.enabled", False)
    profile.update_preferences()
    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path='./geckodriver')
    driver.get("http://www.facebook.com")
    time.sleep(3)
    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("loginbutton").click()
    time.sleep(3)

    for url in urllist:
        driver.get('http://www.facebook.com/' + url)
        htmltext = driver.page_source
        soup = BeautifulSoup(htmltext, 'html.parser')
        for raw_text in soup.select('li[class="_5i_q"]'):
            output += re.findall(re.compile('aria-label="(.*?)" class="_s'),
                                 str(raw_text))

    driver.close()
    return output


# emoji_persons = parse_good_urllist(good_urllist)


def tidy_up_data(post_persons, comment_persons, emoji_persons):

    all_persons = list(set(post_persons+comment_persons+emoji_persons))
    post_times = []
    comment_times = []
    emoji_times = []

    for p in all_persons:
        post_times.append(post_persons.count(p))
        comment_times.append(comment_persons.count(p))
        emoji_times.append(emoji_persons.count(p))

    return pd.DataFrame(dict(成員ID=all_persons, 貼文次數=post_times, 回文次數=comment_times, 回覆表情符號次數=emoji_times))


if __name__ == '__main__':
    '''
    程式參考：
    1. https://freelancerlife.info/zh/blog/python%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2%E6%87%89%E7%94%A8-facebook%E7%A4%BE%E5%9C%98%E6%88%90%E5%93%A1%E5%8F%83%E8%88%87%E5%BA%A6%E5%88%86%E6%9E%90/

    程式說明：
    1. 請先修改帳密
    2. 確認geckodriver路徑
    
    環境：
    1. 此bot請在台灣繁體中文環境執行
    2. 建議先手動登入確認該臉書帳號，是否會跳出任何其它要求確認的畫面，
       如有先將關閉，避免程式誤判
    
    '''
    username = 'username'
    password = 'password'

    htmltext = get_htmltext(username, password)
    post_persons, comment_persons, good_urllist = parse_htmltext(
        htmltext, datetime.datetime(2020, 3, 1), datetime.datetime(2020, 3, 15))
    emoji_persons = parse_good_urllist(username, password, good_urllist)
    df = tidy_up_data(post_persons, comment_persons, emoji_persons)
    df.to_excel('member_activity.xlsx', index=False)

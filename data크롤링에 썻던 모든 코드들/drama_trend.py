from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np
import pymysql
from openpyxl import Workbook
import movie_trend
import google_trend


def drama_trend():
    SCROLL_PAUSE_TIME = 2

    url_watchapedia = "https://pedia.watcha.com/ko-KR"
    url_kinolights = "https://m.kinolights.com/search"
    url_naver = "https://www.naver.com/"

    def parse(t):
        idx, p= str(t).split("   ")
        if 'Name' in p:
            p, _ = str(p).split('Name')
        return p

    def parse_one_space(t):
        res = t
        if ' ' in t:
            res, _ = str(t).split(' ')
        return res

    def parse_info_in_Three(t):
        med = ''
        year, nation, med = str(t).split(' ・ ')
        res = [year, nation, med]
        return res




    write_wb = Workbook()
    write_ws = write_wb.active

    # Chrome drvier 실행
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = wd.Chrome(chrome_options=chrome_options)
    driver.get(url_watchapedia)



    driver.find_element_by_css_selector('#root > div > div.css-1fgu4u8 > header > nav > div > div > ul > li:nth-child(3) > button').click()

    time.sleep(SCROLL_PAUSE_TIME / 2)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    # Get Program Info

    time.sleep(SCROLL_PAUSE_TIME)

    ##추출한 영화 목록
    drama_list = []


    elem = driver.find_elements_by_class_name('css-5yuqaa')
    time.sleep(SCROLL_PAUSE_TIME)
    count = 0
    for i in range(1, 6):
        for j in range(1, 6):
            try:
                #title = driver.find_element_by_css_selector(f'#root > div > div.css-1fgu4u8 > section > div > section > div:nth-child({i}) > div.css-gc1vu8-StyledHorizontalScrollOuterContainer.ebeya3l4 > div > div.css-1nptxmy > div > div > ul > li:nth-child({j}) > a > div.css-ixy093 > div.css-5yuqaa')
                #info = driver.find_element_by_css_selector(f'#root > div > div.css-1fgu4u8 > section > div > section > div:nth-child({i}) > div.css-gc1vu8-StyledHorizontalScrollOuterContainer.ebeya3l4 > div > div.css-1nptxmy > div > div > ul > li:nth-child({j}) > a > div.css-ixy093 > div.css-6t186m-StyledContentYearAndNation.ebeya3l12')
                title = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/section/div/section/div[{}]/div[2]/div/div[1]/div/div/ul/li[{}]/a/div[2]/div[1]'.format(i,j))
                #print("title:", title.text)
                #print("info", info.text)
                #info_list = parse_info_in_Three(info.text)
                if title.text:
                    drama_list.append(title.text)
                    count += 1


                # 검색할 개수 20개
                if count == 20:
                    break
            except:
                break
    # Close Page
    driver.quit()

    # Save xlsx
    #df.to_excel("media_trend.xlsx")
    trend_list = movie_trend.movie_trend(drama_list)

    #trend_list 중복 제거
    result = []

    for value in trend_list:
        if value not in result:
            result.append(value)
    trend_list = result

    return trend_list


    '''

    #DB에 넣기
    connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    media_df = DbToDf(cursor, 'Media')
    #media_list = media_df['mediaName'].values.tolist()


    media_trend_df = google_trend.google_trend(trend_list)

    medianame_list = media_trend_df['이름'].values.tolist()

    connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')
    cursor = connection.cursor()

    for i in range(20):
        try:
            mediaIdx = media_df[media_df['mediaName'] == medianame_list[i]]['idx'].values[0]
        except:
            mediaIdx = -1

        lastInsertId = insertInto(cursor, medianame_list[i], i + 1, mediaIdx)
    '''






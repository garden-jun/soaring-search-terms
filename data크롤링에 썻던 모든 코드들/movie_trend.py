from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime
import re
import pandas as pd
import numpy as np
import pymysql
from openpyxl import Workbook, load_workbook

SCROLL_PAUSE_TIME = 2

url_watchapedia = "https://pedia.watcha.com/ko-KR"
url_kinolights = "https://m.kinolights.com/search"




def parse_one_space(t):
    res = t
    if ' ' in t:
        res, _ = str(t).split(' ')
    return res

def parse_info_in_Three(t):
    year, nation = str(t).split(' ・ ')
    res = [year, nation]
    return res

def parse(t):
    idx, p= str(t).split("   ")
    if 'Name' in p:
        p, _ = str(p).split('Name')
    return p


def movie_trend(drama_list):

    #df = pd.read_excel('media_trend.xlsx')
    write_wb = Workbook()
    write_ws = write_wb.active

    # Chrome drvier 실행
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = wd.Chrome(chrome_options=chrome_options)
    driver.get(url_watchapedia)

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

    time.sleep(SCROLL_PAUSE_TIME / 2)


    time.sleep(SCROLL_PAUSE_TIME)

    title_list = []
    country_list = []
    genre_list = []

    for i in range(2, 7):
        for j in range(1, 6):
            try:
                title = driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/section/div/section/div[{}]/div[2]/div/div[1]/div/div/ul/li[{}]/a/div[2]/div[1]'.format(i, j))
                #info = driver.find_element_by_css_selector(f'#root > div > div.css-1fgu4u8 > section > div > section > div:nth-child({i}) > div.css-gc1vu8-StyledHorizontalScrollOuterContainer.ebeya3l4 > div > div.css-1nptxmy > div > div > ul > li:nth-child({j}) > a > div.css-ixy093 > div.css-6t186m-StyledContentYearAndNation.ebeya3l12')

                #info_list = parse_info_in_Three(info.text)
                #print(title)
                if title.text != '':
                    title_list.append(title.text)
                    #genre_list.append(info_list[0])
                    #country_list.append(info_list[1])
            except:
                continue
    time.sleep(SCROLL_PAUSE_TIME)

    #print(title_list)

    # Close Page
    driver.close()
    trend_list = drama_list + title_list

    return trend_list




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np
import pymysql
import new_mediaActor
import new_mediaImg

## media_Trend 테이블에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor, genreIdx,mediaName,description,screeningYear,country,actorList):
    insertCommand = """ INSERT INTO Media(genreIdx,mediaName,description,screeningYear,country,actorList)
        values ({}, "{}","{}", "{}", "{}", "{}")""".format(genreIdx,mediaName,description,screeningYear,country,actorList)
    lastInsertId = -1

    try:
        cursor.execute("START TRANSACTION")
        cursor.execute(insertCommand)
        cursor.execute("SELECT last_insert_id()")
        lastInsertId = cursor.fetchone()[0]
        cursor.execute("COMMIT")
    except Exception as e:
        print(e)
    return lastInsertId


def DbToDf(cursor, table):
    insertCommand = "select * from {}".format(table)
    try:
        cursor.execute(insertCommand)
        result = cursor.fetchall()
        df = pd.DataFrame(result)
    except:
        print("DB불러오기실패")
    return df


connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8', cursorclass = pymysql.cursors.DictCursor)
cursor = connection.cursor()

media_df = DbToDf(cursor,'Media')
mediaList = media_df['mediaName'].values.tolist()



connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')
cursor = connection.cursor()




def mediaData(all_list):

    # 크롬접속
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #User-agent 변경
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36.")
    driver = webdriver.Chrome(chrome_options = chrome_options)

    All_actor = []

    media_list = []
    for keyword in all_list:
        if keyword in mediaList:
            continue
        print(keyword)
        url = "https://pedia.watcha.com/ko-KR/search?query={}&category=contents".format(keyword)
        driver.get(url)
        time.sleep(3)
        try:
            #driver.find_element_by_css_selector("#root > div > div.css-1fgu4u8 > section > section > div.css-ipmqep-StyledTabContentContainer.e1szkzar3 > div.css-12hxjcc-StyledHideableBlock.e1pww8ij0 > section > section.css-1s4ow07 > div > div.css-1nptxmy > div > ul > li:nth-child(1) > a > div.css-1qmeemv > div > img").click()
            #driver.find_element_by_css_selector("#root > div > div.css-1fgu4u8 > section > section > div.css-ipmqep-StyledTabContentContainer.e1szkzar3 > div.css-12hxjcc-StyledHideableBlock.e1pww8ij0 > section > section.css-1s4ow07 > div > div.css-1nptxmy > div > ul > li:nth-child(1) > a")
            driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/section/section/div[3]/div[1]/section/section[1]/div/div[1]/div/ul/li[1]/a').click()
            print("ND", 1)
        except Exception as e:
            print(e)
            continue
        time.sleep(2)


        # 연도, 국가, 장르
        try:
            media_info = driver.find_element_by_class_name("css-1t00yeb-OverviewMeta.eokm2782").text
            media_info = media_info.replace("·"," ")
            screeningYear, country, genre = map(str,media_info.split())
            genreIdx = GenreIdx(genre)
            print("ND", 2)
        except:
            print("오류2")
            continue

        #description
        try:
            description = driver.find_element_by_class_name("css-kywn6v-StyledText eb5y16b1").text
            description = description.replace('"',"'")
            print("ND", 3)
        except:
            print("오류3")
            description = "no description"

        #Actor
        Actor_list = []
        try:
            AList = driver.find_elements_by_class_name("css-17vuhtq")
            print("ND", 4)
        except:
            print("오류4")
            AList = []

        for AL in AList:
            if AL.text == '':
                continue
            Actor_list.append(AL.text)

        All_actor = All_actor + Actor_list



        media_list.append(keyword)
        lastInsertId = insertInto(cursor,genreIdx, keyword,description,screeningYear,country,Actor_list)
    driver.close()
    #ActorTable 업데이트
    AllActor = []
    for actor in All_actor:
        if actor not in AllActor:
            AllActor.append(actor)
    new_mediaActor.new_mediaActor(AllActor)

    #MediaImg 업데이트
    new_mediaImg.new_mediaImg(media_list)

def GenreIdx(genre):
    genreIdx = 0
    if genre == 'SF':
        genreIdx = 1
    elif genre == '가족':
        genreIdx = 2
    elif genre == '공포(호러)':
        genreIdx = 3
    elif genre == '다큐멘터리':
        genreIdx = 4
    elif genre == '드라마':
        genreIdx = 5
    elif genre == '멜로/로맨스':
        genreIdx = 6
    elif genre == '뮤지컬':
        genreIdx = 7
    elif genre == '미스터리':
        genreIdx = 8
    elif genre == '범죄':
        genreIdx = 9
    elif genre == '사극':
        genreIdx = 10
    elif genre == '서부극(웨스턴)':
        genreIdx = 11
    elif genre == '스릴러':
        genreIdx = 12
    elif genre == '시사/교양':
        genreIdx = 13
    elif genre == '애니메이션':
        genreIdx = 14
    elif genre == '액션':
        genreIdx = 15
    elif genre == '어드벤처':
        genreIdx = 16
    elif genre == '예능':
        genreIdx = 17
    elif genre == '전쟁':
        genreIdx = 18
    elif genre == '코미디':
        genreIdx = 19
    elif genre == '판타지':
        genreIdx = 20
    else:
        genreIdx = 21
    return genreIdx


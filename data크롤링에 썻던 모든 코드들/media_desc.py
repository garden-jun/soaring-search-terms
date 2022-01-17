from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
import numpy as np
import pymysql
import google_trend




## Actor 테이블에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto (cursor, description, mediaName):
    insertCommand = """ UPDATE Media SET description = "{}" WHERE mediaName = "{}" """.format(description, mediaName)
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
media_list = media_df['mediaName'].values.tolist()




connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
cursor = connection.cursor()


count = 0
for keyword in media_list:

    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}".format("영화 " + str(keyword) + " 정보")

    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = wd.Chrome(chrome_options=chrome_options)

    driver.get(url)
    time.sleep(1)

    #decs가져오기
    try:
        desc = driver.find_element_by_class_name("text._content_text").text
    except:
        desc = ""

    if desc == "":
        try:
            desc = driver.find_element_by_class_name("intro_box._content").text
        except:
            desc = ""

    driver.close

    if desc == "":
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}".format(keyword + " 정보")
        driver.get(url)
        try:
            desc = driver.find_element_by_class_name("text.no_ellipsis").text
        except:
            desc = ""


        driver.quit()

    time.sleep(1)

    desc = desc.replace('\"', "\'")


    print(count,"/1229")
    count += 1

    print(keyword)


    lastInsertId = insertInto(cursor,desc, keyword)





from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pymysql
import pandas as pd
import numpy as np


## Actor Table 에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor,actorName, description,imgUrl):
    insertCommand = """ INSERT INTO Actor(actorName, description,imgUrl)
        values ("{}", "{}","{}")""".format(actorName,description,imgUrl)
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

actor_df = DbToDf(cursor,'Actor')
actor_list = actor_df['actorName'].values.tolist()

connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')
cursor = connection.cursor()

def new_mediaActor(all_list):


    # Chrome drvier 실행
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = wd.Chrome(chrome_options=chrome_options)


    for actor in all_list:
        if actor not in actor_list:

            url = "https://www.google.co.kr/search?q={}&hl=ko&tbm=isch&sxsrf=ALeKk01f05FfEQLq8tgid1fo4rMa3TyK2A%3A1627252702018&source=hp&biw=1028&bih=1160&ei=3ef9YJn0O7uYr7wPn9iFGA&oq=&gs_lcp=CgNpbWcQARgAMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnUABYAGC5G2gBcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1nsAEK&sclient=img".format(actor)
            driver.get(url)
            time.sleep(1)
            image = driver.find_element_by_css_selector(".rg_i.Q4LuWd").click()
            time.sleep(1)
            try:
                imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
            except:
                imgUrl = "no img"

            description = actor
            lastInsertId = insertInto(cursor,actor, description,imgUrl)

    driver.close()




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





## Actor 테이블에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto (cursor, exerciseIdx, imgUrl,desc):
    insertCommand = """ INSERT INTO ExerciseImage(exerciseIdx, imgUrl,description)
        values ({}, "{}","{}")""".format(exerciseIdx,imgUrl,desc)
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

exercise_df = DbToDf(cursor,'Exercise')
exercise_list = exercise_df['exerciseName'].values.tolist()




connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
cursor = connection.cursor()


count = 1
for keyword in exercise_list:

    url = "https://www.google.co.kr/search?q={}&hl=ko&tbm=isch&sxsrf=ALeKk01f05FfEQLq8tgid1fo4rMa3TyK2A%3A1627252702018&source=hp&biw=1028&bih=1160&ei=3ef9YJn0O7uYr7wPn9iFGA&oq=&gs_lcp=CgNpbWcQARgAMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnUABYAGC5G2gBcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1nsAEK&sclient=img".format(keyword)

    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = wd.Chrome(chrome_options=chrome_options)

    driver.get(url)
    time.sleep(1)

    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

    exerciseIdx = exercise_df[exercise_df['exerciseName'] == keyword]['idx'].values[0]
    for i in range(5):
        try:
            images[i].click()
            time.sleep(1)
            #imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
            imgUrl = driver.find_element_by_css_selector("#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div > div.OUZ5W > div.zjoqD > div.qdnLaf.isv-id > div > a > img").get_attribute("src")

            lastInsertId = insertInto(cursor, exerciseIdx,imgUrl, keyword)
        except:
            pass


    driver.close()





    print(count,"/83")
    count += 1

    print(keyword)








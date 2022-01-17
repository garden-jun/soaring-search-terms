from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np
import pymysql
import google_trend



def desserttrend_reset(trendlist):
    ## dessertTrend 테이블에 업데이트
    host = "homekiri-new.cws9rsilf8df.ap-northeast-2.rds.amazonaws.com"
    user = 'admin'
    password = 'homekiri0801!'
    database = 'homekiri_new'

    def insertInto (cursor, dessertName, ranking, dessertIdx):
        insertCommand = """ INSERT INTO DessertTrend(dessertName, ranking, dessertIdx)
            values ('{}', {}, {})""".format(dessertName,ranking,dessertIdx)
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

    def deleteTable(cursor, table):
        insertCommand = "TRUNCATE TABLE {}".format(table)
        try:
            cursor.execute(insertCommand)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
        except:
            print("DB삭제 실패")
        return df


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

    dessert_df = DbToDf(cursor,'Dessert')

    deleteTable(cursor,'DessertTrend')


    connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
    cursor = connection.cursor()

    for i in range(len(trendlist)):
        dessertIdx = dessert_df[dessert_df['dessertName'] == trendlist[i]]['idx'].values[0]
        lastInsertId = insertInto(cursor,trendlist[i],i+1,dessertIdx)



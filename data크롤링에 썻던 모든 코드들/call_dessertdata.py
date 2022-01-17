import pandas as pd
import numpy as np
import pymysql
import google_trend
import insta_trend


def call_dessertdata():
    ## dessert 테이블
    host = "homekiri-new.cws9rsilf8df.ap-northeast-2.rds.amazonaws.com"
    user = 'admin'
    password = 'homekiri0801!'
    database = 'homekiri_new'

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
    dessert_list = dessert_df['dessertName'].values.tolist()

    return dessert_list
    #dessertins_list = insta_trend.insta_trend(dessert_list,"먹스타그램")
    #dessertgg_df = google_trend.google_trend(dessertins_list)
    #desserttrend_list = dessertgg_df['이름'].values.tolist()


'''
connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
cursor = connection.cursor()

for i in range(3):
    dessertIdx = dessert_df[dessert_df['dessertName'] == desserttrend_list[i]]['idx'].values[0]
    lastInsertId = insertIntodessert(cursor,desserttrend_list[i],i+1,dessertIdx)
'''


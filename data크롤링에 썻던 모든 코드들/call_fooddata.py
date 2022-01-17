import pandas as pd
import numpy as np
import pymysql
import google_trend
import insta_trend


def call_fooddata():
    ## Food 테이블
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

    food_df = DbToDf(cursor,'Food')
    food_list = food_df['foodName'].values.tolist()

    return food_list
    #foodins_list = insta_trend.insta_trend(food_list,"먹스타그램")
    #foodgg_df = google_trend.google_trend(foodins_list)
    #foodtrend_list = foodgg_df['이름'].values.tolist()


'''
connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
cursor = connection.cursor()

for i in range(3):
    foodIdx = food_df[food_df['foodName'] == foodtrend_list[i]]['idx'].values[0]
    lastInsertId = insertIntoFood(cursor,foodtrend_list[i],i+1,foodIdx)
'''


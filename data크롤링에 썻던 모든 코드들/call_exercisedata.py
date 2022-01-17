import pandas as pd
import numpy as np
import pymysql
import google_trend
import insta_trend


def call_exercisedata():
    ## Exercise 테이블
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

    Exercise_df = DbToDf(cursor,'Exercise')
    Exercise_list = Exercise_df['exerciseName'].values.tolist()

    return Exercise_list
    #Exerciseins_list = insta_trend.insta_trend(Exercise_list,"먹스타그램")
    #Exercisegg_df = google_trend.google_trend(Exerciseins_list)
    #Exercisetrend_list = Exercisegg_df['이름'].values.tolist()


'''
connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
cursor = connection.cursor()

for i in range(3):
    ExerciseIdx = Exercise_df[Exercise_df['ExerciseName'] == Exercisetrend_list[i]]['idx'].values[0]
    lastInsertId = insertIntoExercise(cursor,Exercisetrend_list[i],i+1,ExerciseIdx)
'''


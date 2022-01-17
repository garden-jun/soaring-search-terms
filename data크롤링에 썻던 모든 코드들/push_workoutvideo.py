import pymysql
import pandas as pd
import numpy as np

exercise_df = pd.read_excel('workout_data.xlsx')

## Food_Trend 테이블에 연결
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor, exerciseIdx, videoUrl, description):
    insertCommand = """ INSERT INTO ExerciseVideo(exerciseIdx, videoUrl,description)
        values ({},'{}', '{}')""".format(exerciseIdx,videoUrl,description)
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


connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')
cursor = connection.cursor()


for i in range(83):
    exerimg_desc = exercise_df.iloc[i]['exercise_name']+" img"
    lastInsertId = insertInto(cursor,i+1, exercise_df.iloc[i]['video_url'],exerimg_desc)


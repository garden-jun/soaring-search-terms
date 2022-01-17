import pymysql
import pandas as pd
import numpy as np

workout_df = pd.read_excel('workout_data.xlsx')

## Food_Trend 테이블에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertIntoFood(cursor, typeIdx,difficultyIdx,targetIdx,exerciseName,description):
    insertCommand = """ INSERT INTO Exercise(typeIdx,difficultyIdx,targetIdx,exerciseName,description)
        values ({}, {}, {}, "{}", "{}")""".format(typeIdx,difficultyIdx,targetIdx,exerciseName,description)
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

for i in range(204):
    typeIdx = 0
    if workout_df.iloc[i]['types_name'] == 'Yoga':
        typeIdx = 1
    elif workout_df.iloc[i]['types_name'] == 'Health':
        typeIdx = 2
    elif workout_df.iloc[i]['types_name'] == 'Other':
        typeIdx = 3

    difficultyIdx = 0
    if workout_df.iloc[i]['difficulties_status'] == 'Beginner':
        difficultyIdx = 1
    elif workout_df.iloc[i]['difficulties_status'] == 'Intermediate':
        difficultyIdx = 2
    elif workout_df.iloc[i]['difficulties_status'] == 'Advanced':
        difficultyIdx = 3

    targetIdx = 0
    if workout_df.iloc[i]['targets'] == 'Back':
        targetIdx = 1
    elif workout_df.iloc[i]['targets'] == 'Leg':
        targetIdx = 2
    elif workout_df.iloc[i]['targets'] == 'Full_Body':
        targetIdx = 3
    elif workout_df.iloc[i]['targets'] == 'Arm':
        targetIdx = 4
    elif workout_df.iloc[i]['targets'] == 'Front':
        targetIdx = 5



    lastInsertId = insertIntoFood(cursor,typeIdx, difficultyIdx, targetIdx, workout_df.iloc[i]['exercise_name'],workout_df.iloc[i]['desc'])

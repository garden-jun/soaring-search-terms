import pymysql
import pandas as pd
import numpy as np


## Food_Ingredient Table 에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor,foodIdx, ingredients):
    insertCommand = """ INSERT INTO Food_Ingredient(foodIdx, ingredients)
        values ({}, "{}")""".format(foodIdx,ingredients)
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



ingredients_df = pd.read_excel('Food_ingredient.xlsx')


for i in range(204):
    lastInsertId = insertInto(cursor,i+1, ingredients_df.iloc[i]['all'])

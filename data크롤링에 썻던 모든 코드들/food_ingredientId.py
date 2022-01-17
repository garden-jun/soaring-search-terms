import pymysql
import pandas as pd
import numpy as np


## Food_Trend 테이블에 연결
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor, foodIdx, ingredientIdx):
    insertCommand = """ INSERT INTO Food_Ingredient(foodIdx,ingredientIdx)
        values ({}, {})""".format(foodIdx,ingredientIdx)
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

DF = DbToDf(cursor,'Food')
ingredient_list = DF['ingredient'].values.tolist()

connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')
cursor = connection.cursor()

for i in range(204):
    if ingredient_list[i] == '돼지고기':
        ingredientIdx = 1
    elif ingredient_list[i] == '소고기':
        ingredientIdx = 2
    elif ingredient_list[i] == '닭고기':
        ingredientIdx = 3
    elif ingredient_list[i] == '밥':
        ingredientIdx = 4
    elif ingredient_list[i] == '면':
        ingredientIdx = 5
    elif ingredient_list[i] == '기타':
        ingredientIdx = 7
    else:
        ingredientIdx = 6
    lastInsertId = insertInto(cursor, i + 1, ingredientIdx)






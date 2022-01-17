import pymysql
import pandas as pd
import numpy as np

food_df = pd.read_excel('Food_data.xlsx')

## Food_Trend 테이블에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertIntoFood(cursor, foodName,description,ingredient,recipe,temparture,cookingState,countryIdx):
    insertCommand = """ INSERT INTO Food(foodName,description,ingredient,recipe,temparture, cookingState,countryIdx)
        values ('{}', "{}", '{}', "{}", '{}', "{}", {})""".format(foodName,description,ingredient,recipe,temparture,cookingState,countryIdx)
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
    countIdx = 0
    if food_df.iloc[i]['country'] == 'korea':
        countryIdx = 1
    elif food_df.iloc[i]['country'] == 'jupan':
        countryIdx = 2
    elif food_df.iloc[i]['country'] == 'china':
        countryIdx = 3
    elif food_df.iloc[i]['country'] == 'western':
        countryIdx = 4


    a = food_df.iloc[i]['cookingstate']
    a = a.replace(", ","delim")



    lastInsertId = insertIntoFood(cursor,food_df.iloc[i]['foodName'],food_df.iloc[i]['desc'],food_df.iloc[i]['main_ingredient'],food_df.iloc[i]['recipe'],food_df.iloc[i]['temperature'],a,countryIdx)

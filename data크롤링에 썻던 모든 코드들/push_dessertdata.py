import pymysql
import pandas as pd
import numpy as np

dessert_df = pd.read_excel('dessert_data.xlsx')
dessert_list = dessert_df['dessertName'].values.tolist()
## dessert Table 에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor, drinkIdx,nonDrinkIDx,dessertName,description):
    insertCommand = """ INSERT INTO Dessert(drinkIdx,nonDrinkIDx,dessertName,description)
        values ({}, {}, "{}", "{}")""".format(drinkIdx,nonDrinkIDx,dessertName,description)
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


drink_count = 0
nondrink_count = 0
for i in range(len(dessert_list)):
    drinkIdx = -1
    nonDrinkIdx = -1


    if dessert_df.iloc[i]['drink'] == 'o':
        drink_count += 1
        drinkIdx = drink_count
    elif dessert_df.iloc[i]['drink'] == 'x':
        nondrink_count += 1
        nonDrinkIdx = nondrink_count

    ### 0 ~ 999 Idx 값은 Drink
    ### 1000 ~  Idx 값은 NonDrink


    lastInsertId = insertInto(cursor,drinkIdx,nonDrinkIdx,dessert_df.iloc[i]['dessertName'],dessert_df.iloc[i]['desc'])

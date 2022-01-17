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

#Drink TABLE 에 업데이트
def insertInto(cursor,drinkName,temparture,flavor):
    insertCommand = """ INSERT INTO NonDrink(nondrinkName,temparture,flavor)
        values ("{}", "{}", "{}")""".format(drinkName,temparture,flavor)
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



for i in range(len(dessert_list)):
    if dessert_df.iloc[i]['drink'] == 'x':

        lastInsertId = insertInto(cursor,dessert_df.iloc[i]['dessertName'],dessert_df.iloc[i]['temperature'],dessert_df.iloc[i]['flavor'])

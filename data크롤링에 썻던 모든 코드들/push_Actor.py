import pymysql
import pandas as pd
import numpy as np


## Actor Table 에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor,actorName, description):
    insertCommand = """ INSERT INTO Actor(actorName, description)
        values ("{}", "{}")""".format(actorName,description)
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



media_df = pd.read_excel('media_data.xlsx')
actor_dic = media_df['media_actors_list'].values.tolist()

actorlist=[]
for i in actor_dic:
    if type(i) != float:
        actor = i.split(', ')
        actorlist = actorlist + actor



actor_list = []
for i in actorlist:
    if i not in actor_list:
        actor_list.append(i)



for i in range(len(actor_list)):
    description = actor_list[i]
    lastInsertId = insertInto(cursor,actor_list[i], description)

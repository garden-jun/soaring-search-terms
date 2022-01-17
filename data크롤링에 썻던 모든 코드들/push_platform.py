import pymysql
import pandas as pd
import numpy as np


## Platform Table 에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor,platformName, description):
    insertCommand = """ INSERT INTO Platform(platformName, description)
        values ("{}", "{}")""".format(platformName, description)
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
platform_dic = media_df['platform_name'].values.tolist()

platformlist=[]
for i in platform_dic:
    if type(i) != float:
        platform = i.split(', ')
        platformlist = platformlist + platform



platform_list = []
for i in platformlist:
    if i not in platform_list:
        platform_list.append(i)

print(platform_list)


for i in range(len(platform_list)):
    description = platform_list[i]
    lastInsertId = insertInto(cursor,platform_list[i], description)

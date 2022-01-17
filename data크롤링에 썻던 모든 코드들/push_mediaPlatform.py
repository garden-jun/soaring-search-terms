import pymysql
import pandas as pd
import numpy as np


## Actor Table 에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor,mediaIdx, platformIdx):
    insertCommand = """ INSERT INTO Media_Platform(mediaIdx, platformIdx)
        values ({}, "{}")""".format(mediaIdx,platformIdx)
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


platform_df = DbToDf(cursor,'Platform')
Media_df = DbToDf(cursor, 'Media')




media_df = pd.read_excel('media_data.xlsx')
platform_dic = media_df['platform_name'].values.tolist()
media_name = media_df['media_name'].values.tolist()

platformlist=[]
for i in platform_dic:
    if type(i) != float:
        platform = i.split(', ')
        platformlist.append(platform)
    else:
        platformlist.append("")




connection = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database, charset='utf8')
cursor = connection.cursor()


mediaIdx = -1
for i in range(len(media_name)):

    temp = mediaIdx
    ##미디어 네임과 일치하는 인덱스 찾기
    mediaIdx = Media_df[Media_df['mediaName'] == str(media_name[i])]['idx'].values[0]

    if temp == mediaIdx:    #중복 없애기
        continue

    '''    
    ##플렛폼인덱스에 미디어의 모든 플렛폼인덱스가 들어가는 코드

    platformIdx = ""
    for platformName in platformlist[i]:
        a = str(platform_df[platform_df['platformName'] == platformName]['idx'].values[0])
        if platformIdx == "":
            platformIdx = a
        else:
            platformIdx = platformIdx + "delim" + a

    if platformIdx == "":
        continue

    lastInsertId = insertInto(cursor,mediaIdx, platformIdx)
    '''


    #플렛폼인덱스에 하나의 인덱스값만 들어가는 코드
    for platformName in platformlist[i]:
        platformIdx = platform_df[platform_df['platformName'] == platformName]['idx'].values[0]

        lastInsertId = insertInto(cursor,mediaIdx, platformIdx)

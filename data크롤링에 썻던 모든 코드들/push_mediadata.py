import pymysql
import pandas as pd
import numpy as np

media_df = pd.read_excel('media_data.xlsx')

## media_Trend 테이블에 업데이트
host = 'homekiri-db.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertInto(cursor, genreIdx,mediaName,screeningYear,country,actorList):
    insertCommand = """ INSERT INTO Media(genreIdx,mediaName,screeningYear,country,actorList)
        values ({}, "{}", "{}", "{}", "{}")""".format(genreIdx,mediaName,screeningYear,country,actorList)
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
    genreIdx = 0
    if media_df.iloc[i]['genre_name'] == 'SF':
        genreIdx = 1
    elif media_df.iloc[i]['genre_name'] == '가족':
        genreIdx = 2
    elif media_df.iloc[i]['genre_name'] == '공포(호러)':
        genreIdx = 3
    elif media_df.iloc[i]['genre_name'] == '다큐멘터리':
        genreIdx = 4
    elif media_df.iloc[i]['genre_name'] == '드라마':
        genreIdx = 5
    elif media_df.iloc[i]['genre_name'] == '멜로/로맨스':
        genreIdx = 6
    elif media_df.iloc[i]['genre_name'] == '뮤지컬':
        genreIdx = 7
    elif media_df.iloc[i]['genre_name'] == '미스터리':
        genreIdx = 8
    elif media_df.iloc[i]['genre_name'] == '범죄':
        genreIdx = 9
    elif media_df.iloc[i]['genre_name'] == '사극':
        genreIdx = 10
    elif media_df.iloc[i]['genre_name'] == '서부극(웨스턴)':
        genreIdx = 11
    elif media_df.iloc[i]['genre_name'] == '스릴러':
        genreIdx = 12
    elif media_df.iloc[i]['genre_name'] == '시사/교양':
        genreIdx = 13
    elif media_df.iloc[i]['genre_name'] == '애니메이션':
        genreIdx = 14
    elif media_df.iloc[i]['genre_name'] == '액션':
        genreIdx = 15
    elif media_df.iloc[i]['genre_name'] == '어드벤처':
        genreIdx = 16
    elif media_df.iloc[i]['genre_name'] == '예능':
        genreIdx = 17
    elif media_df.iloc[i]['genre_name'] == '전쟁':
        genreIdx = 18
    elif media_df.iloc[i]['genre_name'] == '코미디':
        genreIdx = 19
    elif media_df.iloc[i]['genre_name'] == '판타지':
        genreIdx = 20

    lastInsertId = insertInto(cursor,genreIdx, media_df.iloc[i]['media_name'],media_df.iloc[i]['media_screening_year'],media_df.iloc[i]['media_country'],media_df.iloc[i]['media_actors_list'])

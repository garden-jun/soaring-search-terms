from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np
import pymysql
import google_trend
import google_trend_atUS
import datetime
#import food_trend_noinsta
#import dessert_trend_noinsta
#import workout_trend_noinsta
import drama_trend
#import dessert_trend_insta
import call_fooddata
import call_exercisedata
import call_dessertdata
import insta_trend
import insta_trend_alltext
import foodtrend_table_reset
import desserttrend_table_reset
import exercisetrend_table_reset
import new_mediaData
import mediatrend_table_reset

days = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']



while True:
    today_day = datetime.datetime.now().weekday()  # 오늘 요일
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    if True:
        #(hour == 1) and (min == 00) :
       #days[today_day] == '일요일' and hour == 15 and min == 3:
        print(datetime.datetime.now())

        ''' 주석내용이 진짜 이걸 고쳐서 써야함.
        #Media Trend
        print("Media Trend 실행")
        mediaTrendList = drama_trend.drama_trend()
        media_trend_list = []
        for media in mediaTrendList:
            if media not in media_trend_list:
                media_trend_list.append(media)
        print(media_trend_list, 1)
        new_mediaData.mediaData(media_trend_list)

        print(media_trend_list)
        # MediaTrend 테이블 업데이트
        mediatrend_table_reset.mediatrend_reset(media_trend_list)
        
        '''
        #이밑에거는 임시방편 인덱스 -1 나옴
        print("Media Trend 실행")
        media_trend_list = drama_trend.drama_trend()
        media_trend_list = media_trend_list[:10]
        mediatrend_table_reset.mediatrend_reset(media_trend_list)
        print(media_trend_list)
        break


















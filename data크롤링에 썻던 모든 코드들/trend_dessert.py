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

days = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']



while True:
    today_day = datetime.datetime.now().weekday()  # 오늘 요일
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    if True:
        #days[today_day] == '목요일' and hour == 1 and min == 3:
        #(hour == 1) and (min == 00) :

        print(datetime.datetime.now())


        #Dessert Trend
        print("Dessert Trend 실행")
        dessert_trend_list = []  # 최종 리스트
        dessert_list = call_dessertdata.call_dessertdata()

        try:
            dessert_insta_list = insta_trend_alltext.insta_trend(dessert_list, "카페스타그램")
        except:
###이부분 바꿔야함 리스트가 아닌 딕셔너리로

            dessert_insta_list = []
            for word in dessert_list:
                dessert_insta_list.append((word, 0))
            print("dessert Instagram 실행 오류")

        ##빈도수순으로 dessert_trend_list 에 넣고 같은 빈도수를 가지면 googleTrends로 상승폭 부여
        google_list = []
        temp = dessert_insta_list[0][1]
        for i in range(len(dessert_insta_list)):
            if dessert_insta_list[i][1] == temp:
                google_list.append(dessert_insta_list[i][0])
                if i == len(dessert_insta_list) - 1:
                    google_trend_list = google_trend.google_trend(google_list)
                    dessert_trend_list = dessert_trend_list + google_trend_list
            else:
                if len(google_list) == 1:
                    dessert_trend_list = dessert_trend_list + google_list
                else:
                    google_trend_list = google_trend.google_trend(google_list)
                    dessert_trend_list = dessert_trend_list + google_trend_list

                temp = dessert_insta_list[i][1]
                google_list = [dessert_insta_list[i][0]]

            if len(dessert_trend_list) >= 10:
                break

        dessert_trend_list = dessert_trend_list[:10]
        print(dessert_trend_list)

        #dessertTrend테이블 업데이트
        desserttrend_table_reset.desserttrend_reset(dessert_trend_list)
        break










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
        #(hour == 1) and (min == 00) :
       #days[today_day] == '일요일' and hour == 15 and min == 3:
        print(datetime.datetime.now())



        #Exercise Trend
        print("Exercise Trend 실행")
        exer_trend_list = [] #최종 트렌드 리스트

        # DB에서 exercise_list 불러오기
        exer_list = call_exercisedata.call_exercisedata()
        exer_google = google_trend_atUS.google_trend(exer_list)

        exer_trend_list = exer_google[:10]
        print(exer_trend_list)

        #workoutTrend 테이블 업데이트
        exercisetrend_table_reset.exercisetrend_reset(exer_trend_list)


        break













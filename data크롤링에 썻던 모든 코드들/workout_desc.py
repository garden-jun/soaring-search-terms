from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np

workout_df = pd.read_excel('workout_data_nodesc.xlsx')

work_list = workout_df['exercise_name'].values.tolist()
workdesc_list = []

for keyword in work_list:

    #음식의 정의 설명 뜻 순으로 검색후 있으면 가져오기
    # definition url
    url = "https://www.google.com/search?q={} description".format(keyword)
    # Chrome drvier 실행
    driver = wd.Chrome("chromedriver.exe")
    driver.get(url)
    time.sleep(2)
    try:
        desc = driver.find_element_by_class_name("hgKElc").text
    except:
        desc = ""
    time.sleep(1)
    driver.quit()

    if desc == "":
        url = "https://www.google.com/search?q={} definition".format(keyword)
        # Chrome drvier 실행
        driver = wd.Chrome("chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        try:
            desc = driver.find_element_by_class_name("hgKElc").text
        except:
            desc = ""
        time.sleep(1)
        driver.quit()

    if desc == "":
        url = "https://www.google.com/search?q={} meaning".format(keyword)
        # Chrome drvier 실행
        driver = wd.Chrome("chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        try:
            desc = driver.find_element_by_class_name("hgKElc").text
        except:
            desc = ""
        time.sleep(1)
        driver.quit()

    workdesc_list.append(desc)

workout_df['desc'] = workdesc_list


###################################엑셀파일 만들기########################
# 결과값 저장
workout_df.to_excel("C:/tempAws/workout_data.xlsx")

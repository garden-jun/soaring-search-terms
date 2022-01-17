from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
import numpy as np


kor_food = ["곱창","대창","막창","된장찌개","김치찌개","청국장찌개","순두부찌개","부대찌개","콩나물국","순대국밥"]#"내장탕","된장국","소고기미역국","김치찜","장조림","오겹살","목살","돼지짜글이","잡채","족발","오리고기","찜닭","대패삼겹살","육개장","돼지두루치기","갈비탕","만둣국","소고기떡국","육전","해물파전","김밥","비빔밥","돌솥비빔밥","볶음밥","덮밥","닭죽","야채죽","쇠고기죽","전복죽","호박죽","닭국수","고기국수","막국수","비빔국수","잔치국수","칼국수","회국수","물냉면","비빔냉면","짜장면","잡채","돼지갈비","소갈비","불고기","돼>지불고기","삽겹살","제육볶음","닭도리탕","삼계탕","치킨","수육","편육","족발","백숙","육회","찜닭","고등어구이","게장","매운탕","물회","오징어볶음","회덮밥",]
#jup_food = ["초밥","스시","라멘","우동","회","돈카츠","소바","텐동","타코야끼","안심까스","와규","규카츠","오뎅","오므라이스","샤브샤브","오꼬노미야끼", "스키야키", "밀푀유나베", "카레", "소고기덮밥", "계란덮밥", "계란찜", "가츠동", "치킨가라아게", "오야꼬동", "타마고산도", "차슈덮밥", "야끼소바", "규동", "오코노미야키", "소고기감자조림", "오야코동", "가라아게", "계란말이","육사시미"]
#china_food = ["지삼선","꿔바로우","완탕면","온면","사천탕면","누룽지","고추잡채","탄탄면","기스면","라조기","팔보채","깐쇼새우","울면","짬뽕밥","양장피","멘보샤","군만두","깐풍기","꽃빵","양꼬치","양갈비","크림새우","칠리새우","유산슬","고추잡채","마파두부","동파육","훠궈", "탕수육", "짜장면", "짬뽕", "깐풍기", "짜장밥", "계란볶음밥", "새우볶음밥", "중국식볶음밥", "볶음밥", "짜장", "마라탕", "짜사이무>침" ,"토마토달걀볶음", "계란볶음밥", "게살볶음밥", "부추잡채"]
#yang_food = ["바질페스토","빠네","스파게티","쇠고기스프","수제버거","바베큐","랍스타","샐러드","리조또","스테이크", "찹스테이크", "그라탕", "오믈렛", "함박스테이크", "프리타타", "라자냐", "연어스테이크", "돈까스", "파스타", "감바스알아히요", "스크램블에그", "피자", "감>바스", "안심스테이크", "감자그라탕", "에그인헬", "퐁듀", "맥앤치즈", "라따뚜이", "등심스테이크", "스크램블", "시금치프리타타", "닭가슴>살스테이크", "만두그라탕", "브루스케타", "치즈오믈렛","생선까스", "고구마그라탕"]

food_list = kor_food + jup_food + china_food + yang_food
food_list = ["라면"]


trand_df = pd.DataFrame("", index=np.arange(1,0), columns=["이름","4주전","3주전","2주전","1주전","이번주","상승도"])


for keyword in food_list:
    url = "https://trends.google.co.kr/trends/?geo=KR"
    # Chrome drvier 실행

    chrome_options = wd.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    driver = wd.Chrome(chrome_options = chrome_options)
    driver.get(url)
    time.sleep(1)

    i = 1
    while(True):
        try:
            elem = driver.find_element_by_css_selector('#input-{}'.format(i))
            elem.send_keys(keyword)
            elem.send_keys(Keys.RETURN)
            break
        except:
            i += 1

    time.sleep(2)
    t = ""
    try:
        t = driver.find_element_by_css_selector('body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(1) > trends-widget > ng-include > widget > div > div > ng-include > div > ng-include > div > line-chart-directive > div.line-chart > div > div:nth-child(1) > div > svg > g:nth-child(2) > g:nth-child(2) > g:nth-child(3) > path').get_attribute("d")
    except:
        pass
    if t == "":
        try:
            t = driver.find_element_by_css_selector('body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(1) > trends-widget > ng-include > widget > div > div > ng-include > div > ng-include > div > line-chart-directive > div.line-chart > div > div:nth-child(1) > div > svg > g:nth-child(2) > g:nth-child(2) > g:nth-child(3) > g > path:nth-child(1)').get_attribute("d")
        except:
            driver.close()
            continue
    A = t.split('L')
    B = []
    for i in A:
        a = i.find(',')
        B.append(float(i[a+1:]))



    MAX = driver.find_element_by_css_selector('body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(1) > trends-widget > ng-include > widget > div > div > ng-include > div > ng-include > div > line-chart-directive > div.line-chart > div > div:nth-child(1) > div > svg > g:nth-child(2) > g:nth-child(2) > g:nth-child(2) > rect').get_attribute("y")
    MIN = driver.find_element_by_css_selector('body > div.trends-wrapper > div:nth-child(2) > div > md-content > div > div > div:nth-child(1) > trends-widget > ng-include > widget > div > div > ng-include > div > ng-include > div > line-chart-directive > div.line-chart > div > div:nth-child(1) > div > svg > g:nth-child(2) > g:nth-child(2) > g:nth-child(1) > rect:nth-child(4)').get_attribute("y")
    MAX = float(MAX)
    MIN = float(MIN)

    rating = []
    for target in B:
        num = 100 - ((target - MIN) / (MAX - MIN)) * 100
        rating.append(round(num))
    trand_row = {
        "이름": keyword,
        "4주전": rating[-5],
        "3주전": rating[-4],
        "2주전": rating[-3],
        "1주전": rating[-2],
        "이번주": rating[-1]
        "상승도": rating[-1] / (rating[-5]*0.1 + rating[-4]*0.2 + rating[-3]*0.3 + rating[-2]*0.4)
    }
    print(keyword)


    '''
    except:
        trand_row = {
            "이름": keyword,
            "4주전": "",
            "3주전": "",
            "2주전": "",
            "1주전": "",
            "이번주": ""
        }
    '''
    driver.close()
    trand_df = trand_df.append(trand_row, ignore_index=True)

trand_df = trand_df.sort_values(by=['상승도'], axis=0,ascending=False)

a = []
b = []
fin = 5

for i in trand_df:
    a.append(i["이름"])
    b.append(i["상승도"])
    if i == fin:
        break

print(a, b)

print(trand_df.head())
#trand_df.to_excel("C:/Users/정원준/OneDrive/바탕 화면/food_data/Food_googletrand.xlsx")





## Food_Trend 테이블에 업데이트
import pymysql
host = 'homekiri.cmi4erzbiz9b.ap-northeast-2.rds.amazonaws.com'
user = 'admin'
password = 'homekiri0801!'
database = 'homekiri'

def insertIntoFood (cursor, foodName, foodIdx):
    insertCommand = """ INSERT INTO food(foodName, fooIdx, updatedAt)
        values ({}, '{}', CURRENT_TIMESTAMP)""".format(foodName,foodIdx)
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



connection = pymysql.connect(host = host, port = 3306, user = user, passwd= password, db = database, charset = 'utf8')
cursor = connection.cursor()

for i in range(5):
    lastInsertId = insertIntoFood(cursor,a[i],b[i])

#print(lastInsertId)
#print(type(lastInsertId))

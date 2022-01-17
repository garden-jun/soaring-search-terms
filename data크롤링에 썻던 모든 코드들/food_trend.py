from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np
import google_trend

word = "먹스타그램"  # 검색창에 검색할 인스타스타
count = 20  # 게시물 갯수

kor_food = ["치킨", "곱창", "대창", "막창", "된장찌개", "김치찌개", "청국장찌개", "순두부찌개", "부대찌개", "콩나물국", "순대국밥", "내장탕", "된장국", "소고기미역국",
            "김치찜", "장조림", "오겹살", "목살", "돼지짜글이", "잡채", "족발", "오리고기", "찜닭", "대패삼겹살", "육개장", "돼지두루치기", "갈비탕", "만둣국",
            "소고기떡국", "육전", "해물파전", "김밥", "비빔밥", "돌솥비빔밥", "볶음밥", "덮밥", "닭죽", "야채죽", "쇠고기죽", "전복죽", "호박죽", "닭국수", "고기국수",
            "막국수", "비빔국수", "잔치국수", "칼국수", "회국수", "물냉면", "비빔냉면", "짜장면", "잡채", "돼지갈비", "소갈비", "불고기", "돼지불고기", "삽겹살",
            "제육볶음", "닭도리탕", "삼계탕", "치킨", "수육", "편육", "족발", "백숙", "육회", "찜닭", "고등어구이", "게장", "매운탕", "물회", "오징어볶음",
            "회덮밥", ]
jup_food = ["초밥", "스시", "라멘", "우동", "회", "돈카츠", "소바", "텐동", "타코야끼", "안심까스", "와규", "규카츠", "오뎅", "오므라이스", "샤브샤브",
            "오꼬노미야끼", "스키야키", "밀푀유나베", "카레", "소고기덮밥", "계란덮밥", "계란찜", "가츠동", "치킨가라아게", "오야꼬동", "타마고산도", "차슈덮밥", "야끼소바",
            "규동", "오코노미야키", "소고기감자조림", "오야코동", "가라아게", "계란말이", "육사시미"]
china_food = ["지삼선", "꿔바로우", "완탕면", "온면", "사천탕면", "누룽지", "고추잡채", "탄탄면", "기스면", "라조기", "팔보채", "깐쇼새우", "울면", "짬뽕밥", "양장피",
              "멘보샤", "군만두", "깐풍기", "꽃빵", "양꼬치", "양갈비", "크림새우", "칠리새우", "유산슬", "고추잡채", "마파두부", "동파육", "훠궈", "탕수육", "짜장면",
              "짬뽕", "깐풍기", "짜장밥", "계란볶음밥", "새우볶음밥", "중국식볶음밥", "볶음밥", "짜장", "마라탕", "짜사이무침", "토마토달걀볶음", "계란볶음밥", "게살볶음밥",
              "부추잡채"]
yang_food = ["바질페스토", "빠네", "스파게티", "쇠고기스프", "수제버거", "바베큐", "랍스타", "샐러드", "리조또", "스테이크", "찹스테이크", "그라탕", "오믈렛",
             "함박스테이크", "프리타타", "라자냐", "연어스테이크", "돈까스", "파스타", "감바스알아히요", "스크램블에그", "피자", "감바스", "안심스테이크", "감자그라탕",
             "에그인헬", "퐁듀", "맥앤치즈", "라따뚜이", "등심스테이크", "스크램블", "시금치프리타타", "닭가슴살스테이크", "만두그라탕", "브루스케타", "치즈오믈렛", "생선까스",
             "고구마그라탕"]

food_list = kor_food + jup_food + china_food + yang_food
bindo = [0] * len(food_list)

# 크롬접속
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
driver = webdriver.Chrome(chrome_options = chrome_options)

driver.get("https://www.instagram.com/")

time.sleep(2)

# 로그인
elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
elem.send_keys('fingercut@naver.com')
elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
elem.send_keys("haeok3013@")
elem.send_keys(Keys.RETURN)

# 팝업창 클릭
time.sleep(5)
driver.find_element_by_class_name("cmbtv").click()
time.sleep(3)
driver.find_element_by_class_name("aOOlW.HoLwm").click()
time.sleep(3)

# 검색창에 검색 및 클릭
driver.find_element_by_class_name("XTCLo.x3qfX").send_keys(word)
time.sleep(5)
a = driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div')
a.click()
time.sleep(8)

# 첫번째 게시글 클릭
driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[2]').click()
time.sleep(5)

# 데이터 기록, 다음 게시물로 클릭
for i in range(count):
    try:
        # 해쉬태그 데이터 기록
        data = driver.find_element_by_css_selector('.C7I1f.X7jCj')
        tag_raw = data.text
        tag = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
        tag = ''.join(tag).replace("#", " ")  # "#" 제거
        tag_data = tag.split()
        print(tag_data)
    except:
        tag_data = "error"

    try:  # 최대 50초까지 기다렸다가, > 모양 클릭하여 다음 게시물로 넘어가기
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a._65Bje.coreSpriteRightPaginationArrow')))
        driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
    except:
        print("크롤링이 비정상적으로 종료되었습니다")
        break

    time.sleep(2)
    print('{}, {}번째 게시물 탐색 완료'.format(time.strftime('%c', time.localtime(time.time())), i + 1))

    for i in range(len(food_list)):
        for j in tag_data:
            if food_list[i] in j:
                bindo[i] += 1
                break
driver.close()

ins = []  ##google 트렌드렙에 돌릴 리스트 명단

# 빈도수 2 이상인것들만 ins 리스트 안에 넣음
for i in range(len(food_list)):
    if bindo[i] > 1:
        ins.append(food_list[i])




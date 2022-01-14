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


def insta_trend(all_list, word):
    count = 20  # 게시물 갯수
    bindo = [0] * len(all_list)

    # 크롬접속
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #User-agent 변경
    #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36.")
    driver = webdriver.Chrome(chrome_options = chrome_options)

    driver.get("https://www.instagram.com/")
    time.sleep(2)

    # 로그인
    elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
    #elem.send_keys('fingercut@naver.com')
    elem.send_keys('garden.jun_crawling')
    time.sleep(2)
    elem = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
    #elem.send_keys("haeok3013@")
    elem.send_keys('wjddnjswns4$')
    time.sleep(2)
    elem.send_keys(Keys.RETURN)

    # 팝업창 클릭
    time.sleep(5)
    try:
        driver.find_element_by_class_name("cmbtv").click()
        time.sleep(3)
    except:
        pass
    try:
        driver.find_element_by_class_name("aOOlW.HoLwm").click()
        time.sleep(3)
    except:
        pass

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
    i = 0
    while(i <= count):
        try:
            # 해쉬태그 데이터 기록
            data = driver.find_element_by_css_selector('.C7I1f.X7jCj')
            tag_raw = data.text
            tag = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
            tag = ''.join(tag).replace("#", " ")  # "#" 제거
            tag_data = tag.split()
            #print(tag_data)
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
        #print('{}, {}번째 게시물 탐색 완료'.format(time.strftime('%c', time.localtime(time.time())), i + 1))

        for k in range(len(all_list)):
            for j in tag_data:
                if all_list[k] in j:
                    bindo[k] += 1
                    break
        print(tag_data)
        i += 1
        if i == count:
            ins = []  ##google 트렌드렙에 돌릴 리스트 명단

            # 1 이상인것들만 ins 리스트 안에 넣음
            for j in range(len(all_list)):
                if bindo[j] >= 1:
                    ins.append(all_list[j])
            if len(ins) < 10:
                print("INSTAGRAM의 DATA가 부족하여 재탐색합니다.")
                i = 0

    driver.close()

    insta_list = {}
    for i in range(len(all_list)):
        insta_list[all_list[i]] = bindo[i]

    instalist = sorted(insta_list.items(),key=lambda x:x[1],reverse=True)

    return instalist



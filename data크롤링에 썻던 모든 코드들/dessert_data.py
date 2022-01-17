from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np


dessert_df = pd.read_excel('dessert.xlsx')

dessert_list = dessert_df['dessertName'].values.tolist()



#이미지url리스트, desc리스트
img_list = []
desc_list = []
#image
for keyword in dessert_list:
    url = "https://www.google.co.kr/search?q={}&hl=ko&tbm=isch&sxsrf=ALeKk01f05FfEQLq8tgid1fo4rMa3TyK2A%3A1627252702018&source=hp&biw=1028&bih=1160&ei=3ef9YJn0O7uYr7wPn9iFGA&oq=&gs_lcp=CgNpbWcQARgAMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnMgcIIxDqAhAnUABYAGC5G2gBcAB4AIABAIgBAJIBAJgBAKoBC2d3cy13aXotaW1nsAEK&sclient=img".format(keyword)

    # Chrome drvier 실행
    driver = wd.Chrome("chromedriver.exe")
    driver.get(url)
    image = driver.find_element_by_css_selector(".rg_i.Q4LuWd").click()
    time.sleep(1)
    imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
    print(imgUrl)
    driver.close()

    img_list.append(imgUrl)

    # 디저트의의 정의 설명 뜻 순으로 검색후 있으면 가져오기
    #url 값
    url = "https://www.google.com/search?q={} 정의".format(keyword)
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
        url = "https://www.google.com/search?q={} 설명".format(keyword)
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
        url = "https://www.google.com/search?q={} 뜻".format(keyword)
        # Chrome drvier 실행
        driver = wd.Chrome("chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        try:
            desc = driver.find_element_by_class_name("hgKElc").text
            print(desc)
        except:
            desc = ""
        time.sleep(1)
        driver.quit()

    desc_list.append(desc)

dessert_df['imgUrl'] = img_list
dessert_df['desc'] = desc_list


#엑셀파일
dessert_df.to_excel("C:/tempAws/dessert_data.xlsx")



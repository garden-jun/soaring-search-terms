from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
import numpy as np


media_df = pd.read_excel('media.xlsx')

media_list = media_df['media_name'].values.tolist()

url_kinolights = "https://m.kinolights.com/search"
media_desc = pd.DataFrame("", index=np.arange(1,0), columns=["media_Name","desc"])

#desc리스트
desc_list = []
count = 1
#image
for keyword in media_list:

    res = []
    res.append(keyword)

    driver = wd.Chrome("chromedriver.exe")
    driver.get(url_kinolights)
    time.sleep(2)

    # find Title
    elem = driver.find_element_by_class_name("hover")
    elem.send_keys("{}".format(keyword))
    elem.send_keys(Keys.RETURN)
    time.sleep(4)

    # 검색된 영화 프로그램중 맞는 영화 검색
    try:
        Notfinded = False
        for temp in driver.find_elements_by_class_name('name'):
            if (temp.text == keyword):
                temp.click()
                time.sleep(2)
                Notfinded = True
                break

        if not Notfinded:
            try:
                print("영화 Notfinded 실행됨")
                driver.find_element_by_css_selector('#contents > div.search-container.hide > section.search-content > section:nth-child(1) > div:nth-child(2) > div > div > div > ul > div > li > a > div > div.info-wrap > h2').click()
                time.sleep(2)
            except:
                print("영화 except문 실행됨")

    except:
        print("Search 영화List Error")

    if not Notfinded:
        # 검색된 TV프로그램중 맞는 TV 검색
        try:
            Notfinded = False
            for i in range(10):
                try:
                    temp = driver.find_element_by_css_selector(
                        f'#contents > div.search-container.hide > section.search-content > section:nth-child(2) > div:nth-child(2) > div > div > div > ul:nth-child({i + 1}) > div > li:nth-child(1) > a > div > div.info-wrap > h2')

                    if (temp.text == keyword):
                        temp.click()
                        time.sleep(2)
                        Notfinded = True
                        break

                    if not Notfinded:
                        try:
                            print("TV Notfinded 실행됨")
                            driver.find_element_by_css_selector(
                                '#contents > div.search-container.hide > section.search-content > section:nth-child(2) > div:nth-child(2) > div > div > div > ul > div > li > a > div > div.info-wrap > h2').click()
                            time.sleep(2)
                        except:
                            print("TV except문 실행됨")
                            driver.close()
                except:
                    continue
        except:
            print("Search TV List Error")

    # PopUp 제거
    time.sleep(4)
    try:
        driver.find_element_by_css_selector(
            '#contents > div.download-modal-mask > div > div > div > button > i').click()
        time.sleep(2)
    except:
        print('No PopUp Element')


    #decs가져오기
    try:
        desc = driver.find_element_by_class_name("synopsis").text
    except:
        desc = ""

    desc = desc.replace('\"',"\'")
    time.sleep(1)
    driver.quit()

    desc_list.append(desc)

    print(count,"/1229")
    count += 1
    row = {
        "media_Name": keyword,
        "desc": desc
    }
    media_desc = media_desc.append(row, ignore_index=True)

media_df['desc'] = desc_list


#엑셀파일
media_df.to_excel("C:/tempAws/media_data.xlsx")



from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
import numpy as np



#google 트렌드 순으로 정렬
def google_trend(trend_list):
    trend_df = pd.DataFrame("", index=np.arange(1,0), columns=["이름","4주전","3주전","2주전","1주전","이번주","상승도"])
    for keyword in trend_list:
        url = "https://trends.google.com/trends/?geo=US"
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
        try:
            trend_row = {
                "이름": keyword,
                "4주전": rating[-5],
                "3주전": rating[-4],
                "2주전": rating[-3],
                "1주전": rating[-2],
                "이번주": rating[-1],
                "상승도": rating[-1] / (rating[-5] * 0.1 + rating[-4] * 0.2 + rating[-3] * 0.3 + rating[-2] * 0.4)
            }
        except:
            trend_row = {
                "이름": keyword,
                "4주전": 0,
                "3주전": 0,
                "2주전": 0,
                "1주전": 0,
                "이번주": 0,
                "상승도": 0
            }
        print(keyword)
        driver.close()
        trend_df = trend_df.append(trend_row, ignore_index=True)

    trend_df = trend_df.sort_values(by=['상승도'], axis=0,ascending=False)
    return trend_df



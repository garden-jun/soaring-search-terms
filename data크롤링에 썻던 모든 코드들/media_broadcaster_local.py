from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np

import google_trend




media_df = pd.read_excel('media_data.xlsx')
media_list = media_df['media_name'].values.tolist()
platform_list = media_df['platform_name'].values.tolist()




for i in range(len(media_list)):
    keyword = str(media_list[i])
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={}".format(keyword+" 방송사")

    # Chrome drvier 실행
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = wd.Chrome(chrome_options=chrome_options)
    driver.get(url)

    time.sleep(1)

    try:
        broadcaster= driver.find_element_by_class_name('info_group')
        broadcaster = broadcaster.text
    except:
        broadcaster = "no broadcaster"

    driver.close()

    if 'JTBC' in broadcaster:
        platform_list[i] = str(platform_list[i]) + ', JTBC'
    elif 'MBC' in broadcaster:
        platform_list[i] = str(platform_list[i]) + ', MBC'
    elif 'KBS' in broadcaster:
        platform_list[i] = str(platform_list[i]) + ', KBC'
    elif 'SBS' in broadcaster:
        platform_list[i] = str(platform_list[i]) + ', SBC'
    elif 'tvN' in broadcaster:
        platform_list[i] = str(platform_list[i]) + ', tvN'
    else:
        pass
    print(i, platform_list[i])

media_df['platform_name'] = platform_list

media_df.to_excel("C:/tempAws/media_broad.xlsx")



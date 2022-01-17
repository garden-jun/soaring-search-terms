from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np

food_df = pd.read_excel('Food_data.xlsx', usecols = ['foodName'])
print(food_df)

food_list = food_df['foodName'].values.tolist()



# dataframe 만들기
Food_df = pd.DataFrame("", index=np.arange(1,0), columns=["foodName","ingredient","source","all"])

for keyword in food_list:
    # 해시태그 url 값
    url = "https://www.10000recipe.com/recipe/list.html?q={}".format(keyword)

    # Chrome drvier 실행
    chrome_options = wd.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    driver = wd.Chrome(chrome_options = chrome_options)
    driver.get(url)
    time.sleep(1)

    #레시피 클릭
    try:
        driver.find_element_by_css_selector("#contents_area_full > ul > ul > li:nth-child(1) > div.common_sp_thumb > a > img").click()
    except:
        continue

    time.sleep(1)
    recipe_ingredient = [] #레시피 재료
    #재료 크롤링
    a = 1
    while(True):
        try:
            ingredient = driver.find_element_by_xpath('//*[@id="divConfirmedMaterialArea"]/ul[1]/a[{}]/li'.format(a))
            ingredient = ingredient.text
            ingredient = ingredient.split("\n")[0]
            recipe_ingredient.append(ingredient)
            a = a + 1
        except:
            break
    print(recipe_ingredient)
    recipe_source = [] #레시피 양념
    #양념 크롤링
    ul = 1
    count = 0
    while(True):
        a = 1
        ul = ul + 1
        temp = count
        while(True):
            try:
                source = driver.find_element_by_xpath('//*[@id="divConfirmedMaterialArea"]/ul[{}]/a[{}]/li'.format(ul,a))
                source = source.text
                source = source.split("\n")[0]
                recipe_source.append(source)
                count += 1
                a = a + 1
            except:
                break
        if temp == count:
            break
    print(recipe_source)

    all = recipe_ingredient + recipe_source
    print(all)
    driver.close()


    #food DB 데이터프레임
    food_row = {
        "foodName":keyword,
       "ingredient": recipe_ingredient,
        "source": recipe_source,
        "all": all
    }
    Food_df = Food_df.append(food_row, ignore_index=True)




###################################엑셀파일 만들기########################
# 결과값 저장
Food_df.to_excel("C:/tempAws/Food_ingredient.xlsx")

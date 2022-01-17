from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
import numpy as np

food_df = pd.read_excel('food.xlsx', usecols = ['foodName', 'Country'])
print(food_df)

food_list = food_df['foodName'].values.tolist()

cow = ["소고기", "한우", "불고기","소갈비"]    #소고기 재료목록
pig = ["돼지", "삼겹살","돈까스","만두","오겹살","목살","항정살"]    #돼지고기 재료목록
chic = ["닭"]                #닭고기 재료목록
sea = ["연어", "고등어","맛살","게","새우","전복","과메기","굴비","광어","꽁치","오징어","홍어","골뱅이","장어","북어","문어"]    #해산물 재료목록



# dataframe 만들기
Food_df = pd.DataFrame("", index=np.arange(1,0), columns=["foodName","country","main_ingredient","img_url","desc","recipe", "temperature", "cookingstate"])

for keyword in food_list:
    # 해시태그 url 값
    url = "https://www.10000recipe.com/recipe/list.html?q={}".format(keyword)

    # Chrome drvier 실행
    driver = wd.Chrome("chromedriver.exe")
    driver.get(url)
    time.sleep(1)

    #레시피 클릭
    try:
        driver.find_element_by_css_selector("#contents_area_full > ul > ul > li:nth-child(1) > div.common_sp_thumb > a > img").click()
    except:
        continue
    #레시피 제목
    title = driver.find_element_by_css_selector("#contents_area > div.view2_summary.st3 > h3")
    recipe_title = title.text
    #음식 이미지 url
    try:
        image = driver.find_element_by_css_selector('#main_thumbs').get_attribute("src")
    except:
        continue


    recipe_ingredient = [] #레시피 재료
    main_ingredient = []
    #재료 크롤링
    a = 1
    while(True):
        try:
            ingredient = driver.find_element_by_xpath('//*[@id="divConfirmedMaterialArea"]/ul[1]/a[{}]/li'.format(a)).text
            ingredient = ingredient.replace("\n", ": ")
            recipe_ingredient.append(ingredient)
            a = a + 1
        except:
            break
    for mai in recipe_ingredient:
        for ingre in pig:
            if ingre in mai:
                main_ingredient.append("돼지고기")
        for ingre in cow:
            if ingre in mai:
                main_ingredient.append("소고기")
        for ingre in chic:
            if ingre in mai:
                main_ingredient.append("닭고기")
        for ingre in sea:
            if ingre in mai:
                main_ingredient.append(ingre)
        if ("밥" in mai) or ("쌀" in mai):
            main_ingredient.append("밥")
        if ("면" in mai) or ("국수" in mai):
            main_ingredient.append("면")
    while '' in main_ingredient:    
	    main_ingredient.remove('')
        
    if main_ingredient == []:
        main_ingredient.append("기타")
    print(main_ingredient)

    recipe_source = [] #레시피 양념
    #양념 크롤링
    a = 1
    while(True):
        try:
            source = driver.find_element_by_xpath('//*[@id="divConfirmedMaterialArea"]/ul[2]/a[{}]/li'.format(a)).text
            source = source.replace("\n", ": ")
            recipe_source.append(source)
            a = a + 1
        except:
            break

    recipe_step = [] #레시피 순서
    #레시피 크롤링
    step = driver.find_element_by_xpath('//*[@id="contents_area"]/div[10]').find_elements_by_class_name("media-body")
    for i in step:
        recipe_step.append(i.text)

    if recipe_step == []:
        step = step = driver.find_element_by_xpath('//*[@id="contents_area"]/div[12]').find_elements_by_class_name("media-body")
        for i in step:
            recipe_step.append(i.text)

    driver.close()

    # 음식나라
    country_df = food_df[food_df['foodName'] == keyword]
    country = country_df['Country'].values[0]


    #음식의 정의 설명 뜻 순으로 검색후 있으면 가져오기
    # 해시태그 url 값
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
        except:
            desc = ""
        time.sleep(1)
        driver.quit()



    #food DB 데이터프레임
    food_row = {
        "country": country,
        'main_ingredient' : main_ingredient,
        "foodName": keyword,
        'desc' : desc,
        "recipe": recipe_step,
        'temperature': " ",
        "cooking_state":"",
        "img_url": image
    }
    Food_df = Food_df.append(food_row, ignore_index=True)




###################################엑셀파일 만들기########################
# 결과값 저장
Food_df.to_excel("C:/tempAws/Food_data.xlsx")

from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

PAUSE_TIME = 2

def update_data(table, keyword):

    stop_words = ['팔로우', '선팔', '맞팔', '좋아요', '소통']

    for word in stop_words:
        if keyword in word:
            return table

    workout_keyword = {
        'Front': ['가슴', '벤치', '복근', '크런치', '푸시업', '푸쉬업','체스트', '딥스', '레그레이즈', '싯업', '윗몸', '플라이', 'pushup'],
        'Arm': ['이두', '삼두', '컬', '어깨', '킥백', '딥스', '트라이셉스', '전완', '푸시업'],
        'Full_Body': ['런닝', '유산소', '등산', '버피', '플랭크', '싸이클', '전신', '자전거'],
        'Leg': ['하체', '다리', '허벅지', '스쿼트', '레그', '런지', '힙', '데드', '브릿지'],
        'Back': ['등', '광배', '풀업', '턱걸이', '데드', '백', '코어', 'pullup', '풀다운', '덤벨로우', '친업' ]
    }

    for target in table.keys():
        for i in workout_keyword[target]:
            if i in keyword:
                table[target] += 1
    return table



if __name__ == '__main__':
    # 해시태그 검색어
    keyword = "운동"
    count = 30

    # 로그인 정보
    username = 'fingercut@naver.com'
    userpw = 'haeok3013@'


    # 해시태그 url 값
    url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

    insta_hash = []
    loginUrl = 'https://www.instagram.com/accounts/login/'

    # Chrome driver 실행
    driver = wd.Chrome("chromedriver.exe")
    driver.get(loginUrl)
    time.sleep(PAUSE_TIME)

    # login
    driver.find_element_by_css_selector('#loginForm > div > div:nth-child(1) > div > label > input').send_keys(username)
    driver.find_element_by_css_selector('#loginForm > div > div:nth-child(2) > div > label > input').send_keys(userpw)
    time.sleep(2)
    driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF').click()
    time.sleep(3)


    # 정보 나중에 저장하기 클릭하고 넘어가기
    driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF').click()
    time.sleep(3)
    # 설정 나중에하기 클릭하고 넘어가기
    driver.find_element_by_css_selector('button.aOOlW.HoLwm').click()
    time.sleep(3)

    # 해시태그 검색 창에 "키워드" 검색
    driver.get(url)
    time.sleep(15)

    # 맨 왼쪽 상단 첫 게시물 클릭
    driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
    time.sleep(3)

    workout_targets = ['Front', 'Arm', 'Full_Body', 'Leg', 'Back']
    result = {}
    for target in workout_targets:
        result.setdefault(target, 0)

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
            for ht in tag_data:
                result = update_data(result, ht)
            print(result)
        except:
            tag_data = "error"
            date_text = "error"

        try:  # 최대 50초까지 기다렸다가, > 모양 클릭하여 다음 게시물로 넘어가기
            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a._65Bje.coreSpriteRightPaginationArrow')))
            driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
        except:
            print("크롤링이 비정상적으로 종료되었습니다")
            driver.quit()

        time.sleep(5)
        print('{}, {}번째 게시물 탐색 완료'.format(time.strftime('%c', time.localtime(time.time())), i + 1))


    print(result)

    # in reverse order

    result = sorted(result.items(), reverse=True, key=lambda item: item[1])

    print(result)

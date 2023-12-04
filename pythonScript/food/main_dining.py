# pip install webdriver_manager
# pip install selenium==4.10
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
from bs4 import BeautifulSoup
import os
import re


''' 0.0.csv import & export '''
# CSV 파일 경로
csv_file_path = 'searchData_new.csv'
output_csv_file = '관광지별음식점.csv'

# CSV 파일을 pandas로 읽기
df = pd.read_csv(csv_file_path, encoding='cp949')

''' 0.1.driver 설정 '''
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(executable_path=ChromeDriverManager().install())  # Chrome driver 자동 업데이트
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
browser.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
browser.get("https://www.diningcode.com/list.dc")
browser.implicitly_wait(5)

''' 0.2.함수'''
# 크롤링
def scraping(iidx):
    food_name = ''
    food_type = ''
    jjim = 0
    longtitude = 0
    latitude = 0
    score = 0
    star = 0
    star_user = 0

    ''' (1) 기본 정보 가져오기 '''
    try:    
        food_name = food_list[data].find_element(By.CSS_SELECTOR,"div.InfoHeader > h2").text #음식점명
        after_dot = food_name.split(".")[-1]
        subparts = after_dot.split()[:-1]
        food_name = ' '.join(subparts)
        # print("음식점 이름: ",food_name)

        food_type = food_list[data].find_element(By.CSS_SELECTOR,"p.Category").text.replace('\n', '') #음식점 카테고리
        food_type = food_type.replace(',', '.')
        # print(food_type)
        longtitude = float(cursor_list[data].get_attribute('data-lng'))
        # print(longtitude)
        latitude = float(cursor_list[data].get_attribute('data-lat'))
        # print(latitude)
        try:
            jjim = food_list[data].find_element(By.CSS_SELECTOR,"div.Rate > p.heart").text
        except Exception as e:
            jjim = ''
        # print("찜 : ",jjim)
        try:
            score = food_list[data].find_element(By.CSS_SELECTOR,"div.Rate > p.Score > span").text
        except Exception as e:
            score = ''
        # print("점수 : ",score)
        try:
            star = food_list[data].find_element(By.CSS_SELECTOR,"div.Rate > p.UserScore").text
            matches = re.findall(r'\d+\.\d+|\d+', star)
            star, star_user = float(matches[0]), int(matches[1])
        except Exception as e:
            star = 0.0
            star_user = 0


    except Exception as e:
        print(e)
    
    '''데이터 저장하기'''
    dict_temp = {
        "food_idx" : iidx,
        "food_id" : id,
        'food_name': food_name,
        'food_type': food_type,
        'food_longtitude':longtitude,
        'food_latitude':latitude,
        'food_jjim' : jjim,
        'food_score' : score,
        'food_star' : star,
        'food_starUser' : star_user
        
        }
    food_dict.append(dict_temp)
    print(f'{food_name} ...완료')

    # TXT 파일에 index 번호 입력
    with open('index_numbers.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(f'{index}\n')

def more():
    try:
        while True:
            more = browser.find_element(By.CSS_SELECTOR,"button.SearchMore.upper")
            browser.execute_script("arguments[0].click();", more)
            print("======더보기 버튼 Click======")
            time.sleep(0.3)

    except Exception as e:
        # print(e)
        print('======더보기 버튼 Error======')


''' 1.0.크롤링 시작'''
# 시작시간
print('[[크롤링 시작...]]')
start = time.time()


# dictionary 생성
food_dict = []

iidx = 0
header_df = pd.DataFrame(columns=['food_idx', 'food_id', 'food_name','food_type','food_longtitude','food_latitude','food_jjim','food_score','food_star','food_starUser'])
header_df.to_csv(output_csv_file, mode='w', index=False, encoding='utf-8-sig')

try:
    for index, row in df.iterrows():
        # if index == 3: break
        # if index < 321: continue
        startone = time.time()
        id = row['content_id']
        search = browser.find_element(By.CSS_SELECTOR, 'div.sc-iBdmCd.kcCZjE.Input__Wrap > input.sc-kFCsca.bZIkjH.Search__Input')
        search.click()
        time.sleep(0.5)
        search.clear() #검색어 초기화

        try :
            key_word = row['naddr1']
            search.send_keys(key_word) #검색어 입력 
            search.send_keys(Keys.ENTER) #엔터버튼 누르기 
            time.sleep(0.5)
            print("======naddr1 키워드 검색함======")
            
            food_list = browser.find_elements(By.CSS_SELECTOR, 'a.sc-ilxdoh.dCXsNO.PoiBlock') # 음식점 리스트
            # body = browser.find_element(By.CSS_SELECTOR, 'body').text
            # print(body)
        
            print("data 없으면 True => ",len(food_list)== 0)
            if len(food_list)== 0 :
                print("======data가 없어서 naddr2로 검색======")
                search.click()
                time.sleep(0.5)
                search.clear() #검색어 초기화
                time.sleep(0.5)
                key_word = row['naddr2']
                search.send_keys(key_word) #검색어 입력 
                search.send_keys(Keys.ENTER) #엔터버튼 누르기 
                time.sleep(0.5)
                print("======naddr2 키워드 검색함======")

                more()#버튼 클릭하기 
                food_list = browser.find_elements(By.CSS_SELECTOR, 'a.sc-ilxdoh.dCXsNO.PoiBlock') # 음식점 리스트
                cursor_list = browser.find_elements(By.CSS_SELECTOR, 'a.Marker')
                print(len(food_list))
                for data in range(len(food_list)):
                    scraping(iidx)
                    iidx+=1
            else:
                more()#버튼 클릭하기 
                food_list = browser.find_elements(By.CSS_SELECTOR, 'a.sc-ilxdoh.dCXsNO.PoiBlock') # 음식점 리스트
                cursor_list = browser.find_elements(By.CSS_SELECTOR, 'a.Marker')
                for data in range(len(food_list)):
                    scraping(iidx)
                    iidx+=1
            

        except Exception as e:
            #검색해도 안 나옴
            print("ERROR!! "*3)
            print(e)
            continue
          
        finally:
            result_df = pd.DataFrame(food_dict)
            # print("[result_df 출력]")
            # print(result_df)
            result_df.to_csv(output_csv_file, mode='a', header=False, index=False, encoding='utf-8-sig')

            food_dict = []
            print(f'[{key_word}데이터 수집 완료]\n소요 시간 :', time.time() - startone)


except Exception as e:
            print(e)
 
finally:
    print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
    browser.quit()  # 작업이 끝나면 창을 닫는다.
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
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


service = Service(executable_path=ChromeDriverManager().install())  # Chrome driver 자동 업데이트
browser = webdriver.Chrome(service=service, options=chrome_options)



browser.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
browser.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")

''' 0.2.함수'''
# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(browser, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        browser.quit()
    return wait

def time_wait_frame(num, code):
    try:
        wait = WebDriverWait(browser, num)
        wait.until(EC.frame_to_be_available_and_switch_to_it(code))
    except Exception as e:
        print(e)
        print("frame 못 찾음")

# frame 변경 메소드
def switch_frame(frame):
    browser.switch_to.default_content()  # frame 초기화
    browser.switch_to.frame(frame)  # frame 변경

 # 크롤링
def scraping(iidx):
    food_name = ''
    food_type = ''
    telephone = ''
    jjim = 0
    address = ''
    longtitude = 0
    latitude = 0

         
    ''' (1) 기본 정보 가져오기 '''
    try:    
        food_name = food_list[data].get_attribute('data-title') #음식점명
        print("음식점 이름: ",food_name)
        food_type = food_list[data].find_element(By.CSS_SELECTOR,".item_tit._title > em").text #음식점 카테고리
        # print(food_type)
        telephone = food_list[data].get_attribute('data-tel') #전화번호
        # print(telephone)
        address = food_list[data].find_element(By.CSS_SELECTOR,'.item_address ').text.replace('주소보기\n', '')
        # print(address)
        longtitude = float(food_list[data].get_attribute('data-longitude'))
        # print(longtitude)
        latitude = float(food_list[data].get_attribute('data-latitude'))
        # print(latitude)
        try:
            jjim = food_list[data].find_element(By.CSS_SELECTOR,"em.u_cnt._cnt").text
        except Exception as e:
            jjim = ''
        # print("찜 : ",jjim)
    except Exception as e:
        print(e)
    
    '''데이터 저장하기'''
    dict_temp = {
        "food_idx" : iidx,
        "food_id" : id,
        'food_name': food_name,
        'food_type': food_type,
        'food_tel' : telephone,
        'food_addr': address,
        'food_longtitude':longtitude,
        'food_latitude':latitude,
        'food_jjim' : jjim,
        }
    food_dict.append(dict_temp)
    print(f'{food_name} ...완료')

    # TXT 파일에 index 번호 입력
    with open('index_numbers.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(f'{index}\n')


''' 1.0.크롤링 시작'''
# 시작시간
print('[크롤링 시작...]')
start = time.time()


# dictionary 생성
food_dict = []

iidx = 0
header_df = pd.DataFrame(columns=['food_idx', 'food_id', 'food_name','food_type','food_tel','food_addr','food_longtitude','food_latitude','food_jjim',])
header_df.to_csv(output_csv_file, mode='w', index=False, encoding='utf-8-sig')

try:
    for index, row in df.iterrows():
        # if index < 667:
        #     continue  
        startone = time.time()
        id = row['content_id']
        browser.implicitly_wait(3)

        try :
            key_word = row['naddr1']+" 음식점"
            browser.get(f"https://m.map.naver.com/search2/search.naver?query={key_word}")
            time.sleep(1)
            food_list = browser.find_elements(By.CSS_SELECTOR, 'li._item._lazyImgContainer') # 음식점 리스트
            body = browser.find_element(By.CSS_SELECTOR, 'body').text
            print(body)
   
            print("data 있어?",len(food_list)== 0)
            if len(food_list)== 0 :
                print("data가 없어서 naddr2로 검색")
                key_word = row['naddr2']+" 음식점"
                browser.get(f"https://m.map.naver.com/search2/search.naver?query={key_word}")
                time.sleep(1)
                food_list = browser.find_elements(By.CSS_SELECTOR, 'li._item._lazyImgContainer') # 음식점 리스트

                for data in range(len(food_list)):
                    scraping(iidx)
                    iidx+=1
            else:
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
            print("--------result_df 출력------------")
            print(result_df)
            result_df.to_csv(output_csv_file, mode='a', header=False, index=False, encoding='utf-8-sig')

            food_dict = []
            print(f'[{key_word}데이터 수집 완료]\n소요 시간 :', time.time() - startone)


except Exception as e:
            print(e)
 
finally:
    print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
    browser.quit()  # 작업이 끝나면 창을 닫는다.
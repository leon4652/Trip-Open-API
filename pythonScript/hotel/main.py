# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# Selenium에서 요소의 로딩이나 조건을 기다릴 때 사용
from selenium.webdriver.support.ui import WebDriverWait
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
# 웹 페이지에서 원하는 요소를 찾지 못했을 때 발생하는 예외
from selenium.common.exceptions import NoSuchElementException
# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
# csv 파일을 다루기 위한 pandas
import pandas as pd

# import chromedriver_autoinstaller
# 크롬드라이버 버전확인
# chrome_ver = chromedriver_autoinstaller.get_chrome_version()
# print(chromedriver_autoinstaller.get_chrome_version())

# 크롬드라이버 설치, 세션 시작
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080') # 윈도우 창 설정
# UserAgent값을 바꿔줌(headless 탐지 막기)
#options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
# options.add_argument("--start-maximized")
# options.add_experimental_option("detach", True)
options.add_argument('--headless')  # headless 모드 활성화 # 백 그라운드에서 실행 
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
# 웹페이지 주소
url = 'https://www.goodchoice.kr/' # 여기어때
driver.get(url)
time.sleep(3)

# 변수 선언
# CSV 파일 경로
csv_file_path = 'searchData.csv'
output_csv_file = '관광지별숙소.csv'
# 결과를 저장할 리스트
results = []
# CSV 파일을 pandas로 읽기
df = pd.read_csv(csv_file_path, encoding='utf-8')

# 함수 정의
# 다음달 15일 클릭하는 함수
def click_date():
    date_btn = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/section[1]/div') # 날짜 선택 버튼
    date_btn.click()
    next_month_btn = driver.find_element(By.CLASS_NAME, 'ui-icon-circle-triangle-e')
    next_month_btn.click()
    day_15_btn = driver.find_element(By.XPATH,  "//table[@class='ui-datepicker-calendar']//a[text()='15']")
    day_15_btn.click()
    day_select_complete_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/button[1]')
    day_select_complete_btn.click()
# 지역주소로 숙소 검색하는 함수
def search_accommodation(addr):
     # 검색창을 여는 버튼, 검색창
    search_open_btn = driver.find_element(By.CSS_SELECTOR, 'button.btn_srch.srch_open')
    search_open_btn.click() # 검색 창을 여는 버튼 클릭
    # search_open_btn.send_keys(Keys.ENTER) # 검색 창을 여는 버튼 클릭

    time.sleep(1)

    # 먼저 add2로 검색 시도
    # 검색 로직    
    search_box = driver.find_element(By.CLASS_NAME, 'srch_bar').find_element(By.CLASS_NAME, 'wrap_inp').find_element(By.TAG_NAME, 'input')
    search_box.clear()
    search_box.send_keys(addr)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
# 검색된 숙소 정보 results리스트에 저장하는 함수
def accommodation_to_results(search_results):
    # 검색 결과가 있을 때 id 및 숙소 정보 추출
    for idx, result in enumerate(search_results):
        # 숙소 정보: 숙소 이름, 숙소 타입, 주소, 별점, 사진, 가격
        # 숙소 이름
        accommodation_name = result.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'strong').text
        # 만약 숙소이름 옆에 뱃지가 있다면
        try:
            if result.find_element(By.CLASS_NAME, 'name').find_element(By.TAG_NAME, 'strong').find_element(By.CLASS_NAME, 'badge'):
                parts = accommodation_name.split("\n")
                modified_string = " ".join(parts[1:]) # 첫째 원소 제외 나머지 부분 선택
                accommodation_name = modified_string
        except NoSuchElementException:
            accommodation_name 
        # 숙소 타입
        accommodation_type = result.find_element(By.CLASS_NAME, 'right_badges').text
        # 숙소 주소
        accommodation_addr = result.find_element(By.XPATH, f'//*[@id="poduct_list_area"]/ul/li[{idx + 1}]/a/div/div[2]/p[2]').text
        # 숙소 별점
        ## 없으면 -1
        try:
            accommodation_score = result.find_element(By.CLASS_NAME, 'score').find_element(By.TAG_NAME,'em').text
        except NoSuchElementException:
            accommodation_score = -1
        # 숙소 사진
        accommodation_pic = result.find_element(By.CLASS_NAME, 'lazy').get_attribute('src')
        # 숙소 가격
        ## 가격은 대실이 p[1], 숙박이 p[2]에 있음 숙박만 사용할거임
        ## 대실 가격과 숙박 가격을 포함하는 부모 요소 찾기
        price_parent_element = result.find_element(By.XPATH, f'//*[@id="poduct_list_area"]/ul/li[{idx + 1}]/a/div/div[3]')
        ## p[2]가 존재하는지 확인
        try:
            accommodation_price = price_parent_element.find_element(By.XPATH, 'p[2]').text
        except NoSuchElementException:
            ## p[2]가 존재하지 않으면 'p'에서 값을 가져옴
            accommodation_price = price_parent_element.find_element(By.XPATH, 'p').text
        # 숙소 위도, 경도
        accommodation_lat = result.find_element(By.TAG_NAME, 'a').get_attribute('data-alat')
        accommodation_lng = result.find_element(By.TAG_NAME, 'a').get_attribute('data-alng')
        # csv에 저장할 결과
        results.append({'id': id, 'accommodation_name': accommodation_name, 'accommodation_type': accommodation_type, 'accommodation_addr': accommodation_addr, 'accommodation_score': accommodation_score, 'accommodation_pic': accommodation_pic, 'accommodation_price': accommodation_price, 'accommodation_lat': accommodation_lat, 'accommodation_lng': accommodation_lng})

# main 함수
# CSV 파일에서 검색어 및 contentId 읽어오기
for index, row in df.iterrows():
    id = row['id']
    addr1 = row['addr1']
    addr2 = row['addr2']        
    
    if index < 19607: 
        continue

    # 지금 몇 번째 관광지에 대한 숙소 검색중인지 print
    print(f'{index}: start')

    # addr2 주소로 숙소 검색하는 함수
    search_accommodation(addr2)
   
    # 다음달 15일 클릭하는 함수
    # click_date()

    # 검색된 숙소 정보가 있다면 정보 results[] 에 저장
    search_results = driver.find_elements(By.CLASS_NAME, 'list_4')    
    if search_results:
        accommodation_to_results(search_results)
    # addr2 검색 결과가 없을 때 addr1로 숙소 검색 시도
    elif driver.find_elements(By.CLASS_NAME, 'result_empty'):
        search_accommodation(addr1)

        # 다음달 15일 클릭하는 함수
        # click_date()

        # 검색된 숙소 정보가 있다면 정보 results[] 에 저장
        search_results = driver.find_elements(By.CLASS_NAME, 'list_4')
        if search_results:
           accommodation_to_results(search_results)
        # addr1 검색 결과가 없다면 다음 관광지에 대한 숙소로 넘어감
        elif driver.find_elements(By.CLASS_NAME, 'result_empty'):
            continue

    # 검색 결과를 pandas DataFrame으로 만들고 CSV 파일에 저장 (인덱스 하나마다 저장)
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_csv_file, mode='a', index=False, encoding='utf-8')
    # 결과 리스트 초기화
    results = []

    # TXT 파일에 index 번호 입력
    with open('index_numbers.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(f'{index}\n')

# 브라우저 종료
driver.quit()
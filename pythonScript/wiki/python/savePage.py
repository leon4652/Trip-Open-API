from datasets import load_dataset
from pymongo import MongoClient
from koreanCheck import remove_non_korean
from textSimilarity import textSimilarity
import pymysql
from MongoDBConnector import MongoDBConnector

# 나무위키 데이터셋 추출
dataset = load_dataset("heegyu/namuwiki")

# mongo db 연결
connector = MongoDBConnector("wiki_HTML")

# mysql 연결 후 관광지 정보 저장
mysqlConnector = pymysql.connect(host='k9b205.p.ssafy.io', user='b205', password='9gi_ssafy_final', db='b205', charset='utf8')
cur = mysqlConnector.cursor()
sql = 'select title from attraction_info'
result = cur.execute(sql)
attractionArr = cur.fetchall()

# 현재 진행이 몇개까지 됐는지 count 변수
cnt = 0

# 모든 관광지에 대해 조회
for title in attractionArr:
    #관광지 이름 추출
    attraction_title = remove_non_korean(title[0])
    print(attraction_title)

    #관광지 매핑 진행 얼마나 됐는지 페이지에 저장
    with open('attraction_index_numbers.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(f'{cnt}\n')
        cnt+=1

    # 나무위키 데이터셋에서 제목과 내용 추출
    for namu in dataset["train"]:
        title = namu["title"]
        content = namu["text"]

        #제목과 관광지 이름 유사도 계산 유사도 55% 넘어야 mongo db에 저장
        if textSimilarity(title, attraction_title) < 0.55:
            continue
        connector.insert_data({
            "attraction":attraction_title, #Root 관광지 이름 저장
            "name":title, #키워드 이름 저장
            "html":content #html text 저장
        })


# print(dataset["train"][1000]["title"])
# print(dataset["train"][1000]["text"])
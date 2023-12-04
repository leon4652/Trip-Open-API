from datasets import load_dataset
from pymongo import MongoClient
from koreanCheck import remove_non_korean
import pymysql
from MongoDBConnector import MongoDBConnector
import re
import pandas as pd
import csv

fromConnector = MongoDBConnector("namu_page")
saveConnector = MongoDBConnector("page")

mysqlConnector = pymysql.connect(host='k9b205.p.ssafy.io', user='b205', password='9gi_ssafy_final', db='b205', charset='utf8')
cur = mysqlConnector.cursor()
sql = f"select ai.content_id, ai.title, ad.overview from attraction_info as ai join attraction_description as ad on ai.content_id = ad.content_id"
result = cur.execute(sql)
attractionArr = cur.fetchall()
attractionDic = {}

cnt = 0

for attraction in attractionArr:
    content_id = attraction[0]
    attractionName = attraction[1]
    overview = attraction[2]
    keywordCnt = 0

    #관광지 매핑 진행 얼마나 됐는지 페이지에 저장
    with open('attraction_index_numbers.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(f'{cnt}\n')
        cnt+=1
    
    #관광지 이름 추출
    stringArr = re.split(r'\s+|\(', attractionName)
    
    newArr = []
    for string in stringArr:
        newArr.append(remove_non_korean(string))
        result = saveConnector.find_data(string)
        if result == None:
            continue
        content = result["content"]
        if "#redirect" in content:
            newKeyword = content[10:]
            content = saveConnector.find_data(newKeyword)

        if content is None:
            continue

        pattern = r'^.*?[목차]'
        content = re.sub(pattern, '', content)
        content = re.sub(r'^.*?목차', '', content)
        
        content = content.replace('[', '')
        content = content.replace(']', '')
        content = content.replace('\n', '')
        content = content.replace('=', '')
        content = re.sub(r'<.*?>', '', content)

        content = re.sub(r'\{\{\{.*?\}\}\}', '', content)

        content = re.sub(r'include\([^)]*\)', '', content)
        content = re.sub(r'\|\| 파일:[^|]+\|\|', '', content)
        content = re.sub(r'파일:[^\s]+\.jpg', '', content)
        content = re.sub(r'파일:[^\s]+\.svg', '', content)
        content = re.sub(r'파일:[^\s]+\.png', '', content)
        content = re.sub(r'width\d+', '', content)
        content = re.sub(r'height\d+', '', content)
        content = re.sub(r'width\d+', '', content)
        content = re.sub(r'width\d+%', '', content)
        content = re.sub(r'height\d+%', '', content)

        content = re.sub(r'파일:[^,]+[.](jpg|svg|png|gif)', '', content)

        content = re.sub(r'https://[^\s]+', '', content)
        content = re.sub(r'http://[^\s]+', '', content)
        content = content.replace('{', '')
        content = content.replace('}', '')
        content = content.replace('|', '')
        content = content.replace('\'', '')
        content = re.sub(r'http\d+$', '', content)

        saveConnector.insert_data({
            "content_id":content_id,
            "attraction_name":attractionName,
            "number": keywordCnt,
            "wiki_title":result['title'],
            "wiki_content":content
        })
        keywordCnt += 1


    if keywordCnt == 0:
        saveConnector.insert_data({
                "content_id":content_id,
                "attraction_name":attractionName,
                "number": "null",
                "wiki_title":"null",
                "wiki_content":"null"
            })


   

        
      

    
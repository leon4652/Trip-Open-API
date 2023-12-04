from datasets import load_dataset
from pymongo import MongoClient
from koreanCheck import remove_non_korean
import pymysql
from MongoDBConnector import MongoDBConnector
import re
import pandas as pd
import csv

mysqlConnector = pymysql.connect(host='k9b205.p.ssafy.io', user='b205', password='9gi_ssafy_final', db='b205', charset='utf8')
cur = mysqlConnector.cursor()
sql = f"select ai.content_id, ad.overview from attraction_info as ai join attraction_description as ad on ai.content_id = ad.content_id"
result = cur.execute(sql)
attractionArr = cur.fetchall()
attractionDic = {}

print("save sql query")
for attraction in attractionArr:
    print(attraction)
    attractionDic[attraction[0]] = attraction[1]

fromConnector = MongoDBConnector("summary_wiki_csv")
connector = MongoDBConnector("summary_overview")

pageList = fromConnector.find_all()

print("mongodb save start")
for page in pageList:
    contentId = page["content_id"]
    # sql = f"select ad.overview from attraction_info as ai join attraction_description as ad where ai.content_id = {contentId}"
    # result = cur.execute(sql)
    # attractionArr = cur.fetchall()
    
    print(contentId)
    overview = ""
    if contentId not in attractionDic:
        overview = "null"
    else:
        overview = attractionDic[contentId]
        if overview is None:
            overview = "null"
        
        overview = overview.replace(",", "")
        overview = overview.replace("，", "")
    
    page["overview"] = overview
    connector.insert_data(page)
from datasets import load_dataset
from pymongo import MongoClient
from koreanCheck import remove_non_korean
import pymysql
from MongoDBConnector import MongoDBConnector
import re
import pandas as pd
import csv

fromConnector = MongoDBConnector("summary_overview")
connector = MongoDBConnector("summary_exact_overview")

pageList = fromConnector.find_all()

memo = {}

for page in pageList:
    flag = False
    attractionName = page["attraction_name"]
    if page["wiki_content"] == "":
        continue

    connector.insert_data(page)
    # attractionName = re.sub(r'\([^)]*\)', '', attractionName)
    # print(attractionName)

    # wikiTitle = page["wiki_title"]
    # nameLen = len(attractionName)
    # checkArr= [attractionName]
    # for i in range(nameLen):
    #     first = attractionName[0:i]
    #     second = attractionName[i:]
    #     checkArr.append(first + " " + second)

    # for check in checkArr:
    #     if check == wikiTitle:
    #         connector.insert_data(page)
    #         flag = True
    #         break
    
    # if flag is False:
    #     page["wiki_content"] = "null"
    #     page["wiki_title"] = "null"
    #     connector.insert_data(page)

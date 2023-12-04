from datasets import load_dataset
from pymongo import MongoClient
from koreanCheck import remove_non_korean
import pymysql
from MongoDBConnector import MongoDBConnector
import re
import pandas as pd
import csv

fromConnector = MongoDBConnector("summary_wiki_page")
connector = MongoDBConnector("summary_wiki_csv")

pageList = fromConnector.find_all()

for page in pageList:
    attractionName= page["attraction_name"]
    wikiTitle = page["wiki_title"] 
    wikiContent = page["wiki_content"]
    attractionName = attractionName.replace(",", "")
    attractionName = attractionName.replace("，", "")
    wikiTitle = wikiTitle.replace(",", "")
    wikiTitle = wikiTitle.replace("，", "")
    wikiContent = wikiContent.replace(",", "")
    wikiContent = wikiContent.replace("，", "")

    page["attraction_name"] = attractionName
    page["wiki_title"] = wikiTitle
    page["wiki_content"] = wikiContent

    connector.insert_data(page)

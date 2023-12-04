from MongoDBConnector import MongoDBConnector
import re

# mongo db 연결
fromConnector = MongoDBConnector("wiki_csv")
namuConnector = MongoDBConnector("namu_page")
connector = MongoDBConnector("wiki_modify")

pageList = fromConnector.find_all()

for page in pageList:
    content = page["wiki_content"]
    

    if "#redirect" in content:
        newKeyword = content[10:]
        content = namuConnector.find_data(newKeyword)

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

    page["wiki_content"] = content

    connector.insert_data(page)
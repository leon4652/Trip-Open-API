import re

def remove_non_korean(text):
    # 한글 아닌 문자 제거
    result = re.sub(r'[^가-힣\s]', '', text)
    return result




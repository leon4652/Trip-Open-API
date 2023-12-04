
def getSummary(text):
    # 시작 문자열과 끝 문자열을 정의합니다.
    start_str = "== 개요 =="
    end_str = "=="
    result = ""

    # 시작 문자열의 위치를 찾습니다.
    start_index = text.find(start_str)

    if start_index != -1:
        # 시작 문자열을 찾았을 때
        # 시작 위치에 시작 문자열의 길이를 더해 끝 문자열의 위치를 찾습니다.
        end_index = text.find(end_str, start_index + len(start_str))

        if end_index != -1:
            # 끝 문자열을 찾았을 때
            # 시작 문자열 다음부터 끝 문자열 이전까지의 부분을 추출합니다.
            result += text[start_index + len(start_str):end_index]
        else:
            print("끝 문자열을 찾을 수 없습니다.")
    else:
        print("시작 문자열을 찾을 수 없습니다.")

    # 시작 문자열과 끝 문자열을 정의합니다.
    start_str = "== 소개 =="
    end_str = "=="

    # 시작 문자열의 위치를 찾습니다.
    start_index = text.find(start_str)

    if start_index != -1:
        # 시작 문자열을 찾았을 때
        # 시작 위치에 시작 문자열의 길이를 더해 끝 문자열의 위치를 찾습니다.
        end_index = text.find(end_str, start_index + len(start_str))

        if end_index != -1:
            # 끝 문자열을 찾았을 때
            # 시작 문자열 다음부터 끝 문자열 이전까지의 부분을 추출합니다.
            result += text[start_index + len(start_str):end_index]
        else:
            print("끝 문자열을 찾을 수 없습니다.")
    else:
        print("시작 문자열을 찾을 수 없습니다.")
    return result
    
    
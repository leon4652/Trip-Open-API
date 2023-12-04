# [개발]셀레니움1

> ref : 
https://mollangpiu.tistory.com/362
[https://velog.io/@rednada1486/Java-Selenium-활용-동적웹크롤링#️-2-selenium과-chromedriver-다운로드](https://velog.io/@rednada1486/Java-Selenium-%ED%99%9C%EC%9A%A9-%EB%8F%99%EC%A0%81%EC%9B%B9%ED%81%AC%EB%A1%A4%EB%A7%81#%EF%B8%8F-2-selenium%EA%B3%BC-chromedriver-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C)
> 

### 셀레니움

Selenium은 웹 브라우저를 자동화하는 도구다. 주로 웹 앱 테스팅에 사용되지만, 크롤링에도 널리 쓰인다. Java, Python 등 여러 언어를 지원하며, 복잡한 웹 페이지에서도 데이터를 추출할 수 있다.

1. **실행 방식**
    - Selenium 코드는 서버 측에서 실행된다. 이 코드는 웹 드라이버 API를 통해 웹 브라우저를 제어한다. 사용자의 로컬 머신에서 크롬을 직접 실행하는 것은 아니다.
2. **크롬 드라이버 필요성**
    - Selenium은 웹 드라이버 인터페이스를 사용해 브라우저를 제어한다. 크롬 드라이버는 이 인터페이스를 크롬 브라우저에 구현한 것이다. 이 드라이버 없이는 Selenium이 크롬 브라우저를 제어할 수 없다.
    

**실제 작동 순서**

1. Spring Boot 애플리케이션에서 Selenium 코드를 실행한다.
2. 해당 코드는 크롬 드라이버를 통해 크롬 브라우저를 제어한다.
3. 웹 페이지에서 필요한 데이터를 수집한 후, 이를 처리하거나 저장한다.

크롬 드라이버는 크롬 브라우저를 제어하기 위한 중개자 역할을 하므로, Selenium 코드와 크롬 브라우저 사이에서 통신을 담당한다.

### 1. Selenium과 Chrome Driver 다운로드

셀레니움

1. https://www.selenium.dev/downloads/ 접속
2. Downloads -> Selenium Server(Grid) -> 4.10.0 클릭

.jar 파일을 직접 넣거나, Gradle을 사용하여 의존성을 추가할 것.

> `implementation 'org.seleniumhq.selenium:selenium-java`
> 

크롬 드라이버

```jsx
1. 자신의 크롬브라우저 버전 체크
(크롬브라우저 열기 -> 점 3개 클릭 -> 설정 -> Chrome 정보)
=> 버전 117.0. .. 크롬 드라이버 버전이 너무 높아 구버전을 맞춰서 따로 설치해야 한다.

2. https://chromedriver.chromium.org/downloads 접속

3. 자신의 크롬브라우저 버전에 맞는 chromedirever 다운
(저는 115버전, 윈도우, 64bit)
```

### 2. Java 프로젝트에 chromedriver 추가

104 버전을 맞춰서 다운로드 받았다.

https://chromedriver.storage.googleapis.com/index.html?path=104.0.5112.79/

https://chromedriver.chromium.org/downloads

### 3. API 문서 따라가기

https://www.selenium.dev/documentation/webdriver/getting_started/install_library/

### 4. 크롤링 우회

여기어때의 경우 크롤링이 되는 경우를 확인, 야놀자의 경우는 차단되었다.

또한 실제 key값이나 한글 검색어에서 URL 인코딩 변경 값을 사용해야 한다.

이 현상은 URL 인코딩(URL Encoding) 또는 퍼센트 인코딩(Percent Encoding)이라고 한다. URL에서는 ASCII 문자셋만 허용되기 때문에, 다른 문자(예: 한글, 공백, 특수문자 등)는 인코딩되어야 한다.

'제주'라는 문자는 UTF-8 형식으로 인코딩되며, UTF-8에서 '제'는 'EC A0 9C'라는 16진수로, '주'는 'EC A3 BC'로 표현된다. 이 16진수 값을 퍼센트 인코딩으로 변환하면 '%EC%A0%9C%EC%A3%BC'가 됩니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/f3272c3b-6f56-47c1-ab79-a5a8fbc8d19f/72e2ab55-65b8-4c7c-a5e6-aeac31a23a72/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/f3272c3b-6f56-47c1-ab79-a5a8fbc8d19f/eafc0061-0bd0-42ca-9501-13a81687bbfb/Untitled.png)

https://blog.hashscraper.com/5-principles-for-bypassing-web-crawling-blocks/

해당 사이트의 방법을 이용해서 우회를 시도해볼 것.

# crawler_server

crawler_server는 네이버, 다음, cgv 등의 영화 정보 사이트에서 데이터를 가져와 한 번에 출력해주는 Onx 웹 사이트 프로젝트에서 사용되는 웹 크롤링 페이지 서버이다.

* Onx 프로젝트의 git 링크 : [Onx](http://github.com/sikurity/Onx)

## 개발 환경
사용 언어는 python 3.6 에서 웹 프레임워크 django 를 사용하였고,
프로젝트의 빌드는 Visual Studio 2015 에서 실행하였다.

### 사용 라이브러리
* BeautifulSoup
* selenium for webdriver(chromedriver)

## 서버 작동 방식

crawler_server는 Onx의 웹 서버에게 크롤링 결과를 JSONObject로 가공해 전달하는 역할을 하며 
Onx 웹 서버에서 url을 통해 요청이 오면 메소드를 실행 후 HttpResponse의 형태로 웹 서버에게 전달한다.  
웹 서버에서 오는 요청과 그 기능을 수행하는 메소드에 맵핑된 url은  
* 검색 키워드를 통해 네이버 영화 사이트에서 검색해 나온 영화 목록 : /crawler/naver_search?title="$검색 키워드"
* 영화 목록 중 하나를 선택해 그 영화의 각 영화 정보 사이트에 있는 영화 정보(평점, 댓글들) : /crawler/commentSearch?title="$영화 제목"&code="$네이버
영화 코드"  
이며, 각 영화 사이트는 네이버 영화, 다음 영화, 익스트림 무비(맥스 무비), cgv 네 개의 사이트를 크롤링한다.  
서버에서 각 사이트에서의 영화 정보를 가져오는 하나의 메소드를 테스트 하는 url은
* /crawler/naver_cinema
* /crawler/daum_search
* /crawler/maxmovie_search
* /crawler/cgv_search
가 존재하며 이들은 웹 서버에서 요청하지는 않는다.  

각 사이트에서의 크롤링 방식은 검색 결과 페이지의 html 구조를 BeautifulSoup 라이브러리를 이용해 각 정보에 맞는 태그를 가진 요소를 추출해 읽어오는 방식인데 
네이버의 경우 영화 목록을 이 사이트에서 가져오므로 검색한 결과를 웹 서버에게 전달할 때 각 영화 정보 페이지의 url 링크를 가져와 웹 서버의 특정 영화의 정보 전달 요청 때 
바로 접근해 크롤링하고 다른 세 개의 사이트의 경우 먼저 웹 서버에서 전달 받은 영화명으로 검색 후 그 페이지에 존재하는 그 영화의 정보의 url을 크롤링으로 추출후 
그 url에 접근해 다시 한 번 크롤링해 영화 정보를 얻어 온다. 이 때, 세 사이트의 페이지에서 스크립트가 로드 되어야 정보를 얻어올 수 있으므로 html 원문을 얻어올 때 
chrome driver를 사용한다.  즉, 웹 서버가 영화 정보를 요청 하면 crawler_server는 총 7번의 페이지 크롤링을 진행해 모든 데이터를 얻는다.  
![crawling method](https://cloud.githubusercontent.com/assets/17040334/25982483/d1fa8b5c-3717-11e7-8f8e-53973bd76a1f.PNG)

## 서버 실행 방법
  1. git의 프로젝트 다운
  2. python을 통해 서버 실행
  3. Onx 웹 서버 실행
  4. http://[server ip]:8080/Onx/ 접근 후 사용
  @ 웹 페이지에 대한 기능은 Onx 프로젝트 README 참조

#-*- coding: utf-8 -*-

"""
author: suchiwon
네이버 영화 사이트를 crawling 하는 메소드를 정의.
검색 키워드를 통해 영화 목록을 얻는 메소드와 한 영화의 정보를 얻는 메소드 2개가 존재.
"""

import cinema_crawler
import cinema

"""
author: suchiwon
네이버 사이트의 검색에서의 영화 목록 결과를 얻어오는 메소드.
JSONObject 형식으로 반환
반환 JSONObject 형식:
{"ID":"정의 id(사용하지 않음"),"Type":"정의 type(사용하지 않음)","Cinemas":[cinema JSONArray]}
"""
def func_naver_search(search_word, start_page, end_page):

    #네이버의 검색 url에서 사용하는 euc-kr 인코딩을 확인하기 위한 변수. 현재는 사용하지 않음
    #encode_byte = str(bytes(search_word,'euc-kr'))

    #crawling 기능 클래스 객체 생성
    crawler_instance = cinema_crawler.Crawler('http://movie.naver.com/',
                                            'movie/search/result.nhn?section=movie&query=',
                                            search_word)

    #request paramter에서 얻은 시작 페이지의 위치부터 시작하도록 지정
    page_idx = start_page

    title_list_saver = []           #한 페이지의 영화 리스트를 저장하는 리스트. 페이지의 결과 비교용.
    total_title_list = []           #모든 페이지의 결과를 저장하는 리스트.

    #모든 페이지의 검색이 끝날 때까지 반복
    while True:

        #네이버 영화 검색 url를 생성. 페이지 parameter를 변경.
        uri = crawler_instance.getPullUrl()
        uri += '&page='
        uri += str(page_idx)
        print(uri)

        try:

            #crawling한 페이지의 html 파싱 데이터 설정
            crawler_instance.setSoup(uri, False)

            #파싱된 데이터에서 각 요소 추출.
            title_list = crawler_instance.getSelector('ul.search_list_1 > li > dl > dt > a')
            point_list = crawler_instance.getSelector('em.num')
            cuser_cnt_list = crawler_instance.getSelector('em.cuser_cnt')
            etc_list = crawler_instance.getSelector('dd.etc')
            image_url_list = crawler_instance.getSelector('p.result_thumb > a > img')
            redirect_url_list = crawler_instance.getSelector('p.result_thumb > a')

            ###
            #현재 페이지의 영화 목록과 이전 페이지의 영화 목록이 같다면 마지막 페이지를 2번 검색했다는 결과이므로
            #전체 목록에 추가하지 않고 break
            if title_list == title_list_saver:
                break

            #현재 페이지의 영화 목록 리스트를 탐색하기 위한 인덱스 변수
            idx = 0

            #영화 목록 리스트를 처음부터 끝까지 탐색
            while idx < len(title_list):

                #각 영화의 정보 요소를 네이버 사이트의 형식에 맞춰 추출.
                title = title_list[idx].get_text().split('(')[0]
                point = float(point_list[idx].get_text())
                cuser_cnt = int(cuser_cnt_list[idx].get_text()[4:-2])
                info = etc_list[2 * idx].get_text()
                actor_info = etc_list[2 * idx + 1].get_text()
                image_url = image_url_list[idx].get('src')
                code = int(str(redirect_url_list[idx].get('href')).split('=')[1])

                #실제 평과 관객이 존재하는 영화만 저장
                if cuser_cnt > 0:

                    #전체 영화 리스트에 클래스를 생성해 저장
                    total_title_list.append(cinema.Cinema(title, point, cuser_cnt, 
                                                          info, actor_info, image_url, code))
                #영화 리스트의 인덱스 증가
                idx = idx + 1

        except Exception as e:
            raise e

        #페이지의 인덱스 증가
        page_idx += 1

        #설정한 마지막 페이지까지 탐색했을 경우 종료
        if (page_idx > end_page):
            break

        #현재 페이지의 결과를 다음 페이지와의 비교를 위해 저장
        title_list_saver = title_list

    #검색한 전체 영화를 중요도순으로 정렬. 정렬 기준은 평가 관객 수를 오름차순으로 정렬.
    total_title_list.sort(reverse=True, key = cinema.Cinema.getKey)

    #JSONObject의 생성을 위한 클래스 생성
    provision = cinema.CinemasProvision(total_title_list)

    #provision 클래스를 통해 JSON 객체 생성
    json_list = crawler_instance.makeJson(provision)
    print("NAVER SEARCH END")

    return json_list

"""
author: suchiwon
네이버 사이트의 특정 영화의 정보 결과를 얻어오는 메소드
JSONObject 형식으로 반환
반환 JSONObject 형식:
{"site_type":"영화 사이트 종류","url":"사이트의 url","point":"영화의 사이트에서의 평점","comments":[댓글 JSONArrary]}
"""
def func_naver_search_one_cinema(redirect_code):

    #crawling 기능 클래스 객체 생성
    crawler_instance = cinema_crawler.Crawler('http://movie.naver.com/',
                                            'movie/search/result.nhn?section=movie&query=',
                                            '')

    #특정 영화 정보 사이트 url 지정
    redirect_url = 'http://movie.naver.com/movie/bi/mi/basic.nhn?code=' + str(redirect_code)

    try:
        #crawling 결과를 html로 파싱한 결과 저장
        soup = crawler_instance.setSoup(redirect_url, False)

        #댓글 및 평점의 정보의 각 요소를 추출해 저장할 리스트
        cinema_point_list = []
        user_point_list = []
        user_id_list = []
        review_list = []
        datetime_list = []                                        
        
        #댓글 및 평점의 각 요소를 네이버 사이트에 맞게 추출
        if soup != None:
            cinema_point_list = soup.select('div.star_score > em')
            user_point_list = soup.select('div.star_score > em')
            user_id_list = soup.select('div.score_reple > dl > dt > em > a > span')
            review_list = soup.select('div.score_reple > p')
            datetime_list = soup.select('div.score_reple > dl > dt > em')

        #영화 평점을 초기화. -1의 경우 검색 실패 플래그로 사용
        cinema_point = -1

        ###
        #영화 평점과 유저 점수의 태그가 같을 경우 구분을 위해 사용.
        #네이버의 경우 같은 태그를 사용하므로 필요.
        cinema_point_idx_offset = 0

        #영화 평점 태그에 해당하는 데이터가 없을 경우 검색 실패로 간주
        if len(cinema_point_list) > 0:

            ###
            #네이버의 경우의 평점 정보 처리.
            #같은 클래스의 태그로 평점의 한 문자(8.01의 경우 8,.,0,1)의 이미지 출력을 위해 넣은 요소와 
            #평점을 그대로 가진 요소가 같이 존재하므로 평점을 가진 요소를 가져오게 함.
            #구분 방식은 요소의 text의 길이가 1보다 크면(네이버의 경우 평점을 8.01의 형식으로 지정)
            #그것을 실제 평점으로 간주
            while cinema_point < len(cinema_point_list):
                point_text = cinema_point_list[cinema_point_idx_offset].get_text().strip()

                if len(point_text) > 1:
                    cinema_point = float(point_text)
                    break

                cinema_point_idx_offset += 1
        #평점 태그에 맞는 요소가 없을 경우 평점을 0점으로 처리
        else:
            cinema_point = 0
        print(cinema_point)

        idx = 0

        #댓글 저장 리스트 초기화
        total_comment_list = []

        #추출한 댓글의 유저 id 리스트 크기만큼 반복해 댓글 요소를 가져와 저장
        while idx < len(user_id_list):
            if len(user_point_list) > idx + cinema_point_idx_offset + 2:
                user_point = int(user_point_list[idx + cinema_point_idx_offset + 2].get_text())
            user_id = user_id_list[idx].get_text().strip()
            review = review_list[idx].get_text().strip()
            datetime = datetime_list[idx * 2 + 1].get_text().strip()

            total_comment_list.append(cinema.Comment(user_id, review, user_point, datetime))

            idx += 1

        #영화 정보를 JSON으로 생성 후 전달
        commentsProvision = cinema.CommentsProvision('naver', redirect_url, cinema_point, total_comment_list)
                                            
        json_list = crawler_instance.makeJson(commentsProvision)
        print("NAVER SEARCH END")
        return json_list

    except Exception as e:
        raise e

    print("NAVER SEARCH FAILED")

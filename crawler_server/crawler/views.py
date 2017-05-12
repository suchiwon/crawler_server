from django.http import HttpResponse
from urllib.parse import quote
import sys
import os
import json

"""
author: suchiwon
func 폴더의 사이트 crawl 관련 메소드 정의 python 파일을 import 하기 위한 경로.
sys에 경로를 추가하여 import
"""
base_path = os.path.dirname( os.path.abspath( __file__ ) )
sys.path.insert(0, base_path + '\\func')
import naver_search
import daum_search
import maxmovie_search
import cgv_search

"""
author: suchiwon
기본 경로(/crawler/). 사용하지 않음.
"""
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

"""
author: suchiwon
네이버 영화 목록 검색 페이지의 crawling 페이지 요청.
경로 맵핑(/crawler/naver_search)
requset parameter: title=(검색 키워드)&start_page=(검색 시작 페이지)&end_page=(검색 끝 페이지)
현재 start_page, end_page는 웹 서버의 UI 제한에 의해 1, 1로 받고 있음
"""
def naver_search_request(request):

    #print(request)

    #request paramter 중 start_page, end_page를 추출. 값이 없을 경우 각각 1, start_page로 지정
    start_page = int(request.GET.get('start_page')) if request.GET.get('start_page') else 1
    end_page = int(request.GET.get('end_page')) if request.GET.get('end_page') else start_page

    ###
    #request paramter 중 title을 추출. 웹서버에서 euc-kr로 인코딩 되어 전달되므로 
    #그 코드를 그대로 사용하기 위해 request url string을 분해하는 형식으로 추출
    #/crawler/naver_search?title=#encoded_title&start_page=1 형식으로 url이 전달될 경우
    #맨 처음 request parameter의 = 문자를 통해 분해하고 뒤의 paremeter와의 구분자 &를 통해 다시 분해해 얻어낸다.
    title = str(request).split('=')[1].split('\'>')[0].split('&')[0]

    #시작, 끝 페이지의 값이 잘못되었을 경우 보정
    if (start_page <= 0):
        start_pqge = 1
    if (end_page < start_page):
        end_page = start_page

    return HttpResponse( naver_search.func_naver_search(title, start_page, end_page) )

"""
author: suchiwon
다음 영화 사이트의 특정 영화의 평점 및 정보 페이지의 crawling 페이지 요청.
경로 맵핑(/crawler/daum_search)
request parameter: title=(영화의 제목)
"""
def daum_search_request(request):

    #print(request)
    
    ###
    #request paramter 중 title을 추출. 웹서버에서 원문으로 전달되므로 
    #그 코드를 그대로 사용하기 위해 request url string을 분해하는 형식으로 추출
    #맨 처음 request paramter의 구분자 = 문자를 통해 분해해 추출
    title = str(request).split('=')[1].split('\'')[0]

    print(title)

    return HttpResponse( daum_search.func_daum_search(title) )

"""
author: suchiwon
맥스무비(익스트림 무비) 사이트의 영화의 특정 영화의 평점 및 정보 페이지의 crawling 페이지 요청.
경로 맵핑(/crawler/maxmovie_search)
request parameter: title=(영화의 제목)
"""
def maxmovie_search_request(request):

    #print(request)
    
    ###
    #request paramter 중 title을 추출. 웹서버에서 원문으로 전달되므로 
    #그 코드를 그대로 사용하기 위해 request url string을 분해하는 형식으로 추출
    #맨 처음 request paramter의 구분자 = 문자를 통해 분해해 추출
    title = str(request).split('=')[1].split('\'')[0]

    print(title)

    return HttpResponse( maxmovie_search.func_maxmovie_search(title) )

"""
author: suchiwon
cgv 사이트의 영화의 특정 영화의 평점 및 정보 페이지의 crawling 페이지 요청.
경로 맵핑(/crawler/cgv_search)
request parameter: title=(영화의 제목)
"""
def cgv_search_request(request):
    
    #print(request)
    
    ###
    #request paramter 중 title을 추출. 웹서버에서 원문으로 전달되므로 
    #그 코드를 그대로 사용하기 위해 request url string을 분해하는 형식으로 추출
    #맨 처음 request paramter의 구분자 = 문자를 통해 분해해 추출
    title = str(request).split('=')[1].split('\'')[0]

    print(title)

    return HttpResponse( cgv_search.func_cgv_search(title) )

"""
author: suchiwon
네이버 사이트의 영화의 특정 영화의 평점 및 정보 페이지의 crawling 페이지 요청.
경로 맵핑(/crawler/naver_search_one_cinema)
request parameter: redirect_url=(네이버 영화 정보 페이지 url)
"""
def naver_search_one_cinema_request(request):

    #print(request)
    
    url = str(request.GET.get('redirect_url'))

    return HttpResponse( naver_search.func_naver_search_one_cinema(url) )

"""
author: suchiwon
위의 네 개의 사이트의 영화의 특정 영화의 평점 및 정보 페이지의 crawling 결과(JSONObject)를
JSONArray 형식으로 묶어 웹서버에 전달하는 페이지 요청.
경로 맵핑(/crawler/commentSearch)
request parameter: title=(평점 및 댓글을 읽어올 영화의 제목)&code=(네이버 사이트에서 영화에게 부여한 code)
"""
def comment_search_request(request):
    
    ###
    #JSONArray 형식의 첫 글자 지정
    comment_result_list = '['

    print(request.GET.get('title'))

    ###
    #네이버 이외의 사이트에서 검색할때 사용할 영화 제목 추출.
    #영화의 제목은 웹서버에서 원문으로 전달.
    #utf-8 인코딩이 될 경우 인코딩 string을 사용할 수 있게 처리
    title = bytes(request.GET.get('title'),'utf-8').decode('utf-8')

    #네이버의 검색을 위한 영화 code 추출.
    redirect_code = request.GET.get('code')

    ###
    #네 개의 사이트에서의 crawling을 통한 영화의 평점 및 댓글을 JSONObject 형식으로 내보낸 결과를 
    #JSONArray 형식으로 연결.
    #하나의 영화 정보의 JSONObject 형식:
    #{"site_type":"영화 사이트 종류","url":"사이트의 url","point":"영화의 사이트에서의 평점","comments":[댓글 JSONArrary]}
    #댓글 JSONArray 내의 한 개의 JSONObject 형식:
    #{"user_id":"유저 아이디","point":"유저가 준 점수","comment":"댓글 내용","datetime":"댓글 게시 시간"}
    comment_result_list += naver_search.func_naver_search_one_cinema(redirect_code)
    comment_result_list += ','
    comment_result_list += daum_search.func_daum_search(title)
    comment_result_list += ','
    comment_result_list += maxmovie_search.func_maxmovie_search(title)
    comment_result_list += ','
    comment_result_list += cgv_search.func_cgv_search(title)
    comment_result_list += ']'

    return HttpResponse( comment_result_list )


from django.http import HttpResponse
from urllib.parse import quote
import sys
import os
import json

##func 폴더의 사이트 crawl 관련 메소드 정의 python 파일을 import 하기 위한 경로.
##sys에 경로를 추가하여 import
base_path = os.path.dirname( os.path.abspath( __file__ ) )
sys.path.insert(0, base_path + '\\func')

import naver_search
import daum_search
import maxmovie_search
import cgv_search

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def naver_search_request(request):

    print(request)

    start_page = int(request.GET.get('start_page')) if request.GET.get('start_page') else 1
    end_page = int(request.GET.get('end_page')) if request.GET.get('end_page') else start_page

    title = str(request).split('=')[1].split('\'>')[0].split('&')[0]

    #title = bytes(title,'utf-8').decode('utf-8')

    #title = bytes(request.GET.get('title'),'utf-8').decode('utf-8')

    if (start_page <= 0):
        start_pqge = 1

    if (end_page < start_page):
        end_page = start_page

    return HttpResponse( naver_search.func_naver_search(title, start_page, end_page) )

def daum_search_request(request):
    print(request)
    
    title = str(request).split('=')[1].split('\'')[0]

    print(title)

    return HttpResponse( daum_search.func_daum_search(title) )

def maxmovie_search_request(request):
    print(request)
    
    title = str(request).split('=')[1].split('\'')[0]

    print(title)
    return HttpResponse( maxmovie_search.func_maxmovie_search(title) )

def cgv_search_request(request):
    print(request)
    
    title = str(request).split('=')[1].split('\'')[0]

    print(title)
    return HttpResponse( cgv_search.func_cgv_search(title) )

def naver_search_one_cinema_request(request):
    print(request)
    
    url = str(request.GET.get('redirect_url'))

    return HttpResponse( naver_search.func_naver_search_one_cinema(url) )

def comment_search_request(request):
 
    #comment_result_list = []
    comment_result_list = '['

    #encoded_title = str(request).split('title=')[1].split('&')[0].eplit('\'>')[0]

    print(request.GET.get('title'))

    title = bytes(request.GET.get('title'),'utf-8').decode('utf-8')
    #title = bytes(encoded_title,'utf-8').decode('utf-8')
    redirect_code = request.GET.get('code')

    comment_result_list += naver_search.func_naver_search_one_cinema(redirect_code)
    comment_result_list += ','
    comment_result_list += daum_search.func_daum_search(title)
    comment_result_list += ','
    comment_result_list += maxmovie_search.func_maxmovie_search(title)
    comment_result_list += ','
    comment_result_list += cgv_search.func_cgv_search(title)
    comment_result_list += ']'

    #json_list = json.dumps(comment_result_list, default=methodcaller("json"), ensure_ascii=False)
    return HttpResponse( comment_result_list )
    #return HttpResponse( json_list )

from django.http import HttpResponse
from urllib.parse import quote
import sys
import os
import json
from operator import methodcaller

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

    title = bytes(request.GET.get('title'),'utf-8').decode('utf-8')

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
    comment_result_list = []

    title = bytes(request.GET.get('title'),'utf-8').decode('utf-8')
    redirect_url = request.GET.get('redirectURL')

    comment_result_list.append( naver_search.func_naver_search_one_cinema(redirect_url) )
    comment_result_list.append( daum_search.func_daum_search(title) )
    comment_result_list.append( maxmovie_search.func_maxmovie_search(title) )
    comment_result_list.append( cgv_search.func_cgv_search(title) )

    #json_list = json.dumps(comment_result_list, default=methodcaller("json"), ensure_ascii=False)
    return HttpResponse( comment_result_list )

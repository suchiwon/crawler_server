from django.http import HttpResponse
from urllib.parse import quote
import sys

sys.path.insert(0,'C:\\Users\\search1\\Documents\\Visual Studio 2015\\Projects\\crawler_server\\crawler_server\\crawler\\func')

import naver_search
import daum_search

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def naver_search_request(request):
    print(request)
    title = str(request).split('=')[1].split('\'')[0]

    return HttpResponse( naver_search.func_naver_search(title) )

def daum_search_request(request):
    return HttpResponse(daum_search.daum_search('범죄와의 전쟁'))

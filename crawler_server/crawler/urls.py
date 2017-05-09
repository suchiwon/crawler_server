from django.conf.urls import url

from . import views

"""각 사이트의 한 영화의 정보(평점, 댓글), 네이버 기반 영화명 검색 리스트를 가져오는 request용 url 맵핑"""
urlpatterns = [
    url(r'^$', views.index, name='index'),                                                          #기본 페이지. 사용하지 않음.
    url(r'^naver_search',views.naver_search_request, name='naver_search'),                          #네이버의 영화 검색 리스트를 crawling해서 받아오는 기능 url
    url(r'^daum_search',views.daum_search_request, name='daum_search'),                             #다음의 특정 영화의 정보를 crawling해서 받아오는 기능 url
    url(r'^maxmovie_search',views.maxmovie_search_request, name='maxmovie_search'),                 #익스트림 무비의 특정 영화의 정보를 crawling해서 받아오는 기능 url
    url(r'^cgv_search',views.cgv_search_request, name='cgv_search'),                                #cgv의 특정 영화의 정보를 crawling해서 받아오는 기능 url
    url(r'^naver_cinema',views.naver_search_one_cinema_request, name='naver_search_one_cinema'),    #네이버의 특정 영화의 정보를 crawling해서 받아오는 기능 url
    url(r'^commentSearch',views.comment_search_request, name='comment_search'),                     #위의 네 개의 사이트의 결과를 하나의 JSONArray로 묶어 웹 서버에 전달하는 url.                                                                                                  
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^naver_search',views.naver_search_request, name='naver_search'),
    url(r'^daum_search',views.daum_search_request, name='daum_search'),
    url(r'^maxmovie_search',views.maxmovie_search_request, name='maxmovie_search'),
    url(r'^cgv_search',views.cgv_search_request, name='cgv_search'),
    url(r'^naver_cinema',views.naver_search_one_cinema_request, name='naver_search_one_cinema'),
    url(r'^commentSearch',views.comment_search_request, name='comment_search'),
]
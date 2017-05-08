from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^naver_search',views.naver_search_request, name='naver_search'),
    url(r'^daum_search',views.daum_search_request, name='daum_search'),
]
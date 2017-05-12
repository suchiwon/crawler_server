"""
Definition of urls for crawler_server.

서버 내의 app들의 내부 urls의 url 경로 맵핑 지정.
현재 서버의 app은 crawler app이 존재한다.
"""

from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', crawler_server.views.home, name='home'),
     url(r'^crawler/', include('crawler.urls')),            #crawler app 내부 url 맵핑 연결

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]

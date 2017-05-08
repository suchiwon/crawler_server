#-*- coding: euc-kr -*-

import sys
import requests
import lxml

from bs4 import BeautifulSoup
from cinema import cinema

def cgv_search(movie_name):

    movie_name = '범죄와의 전쟁 : 나쁜놈들 전성시대'
    name_utf = movie_name.encode('utf8')

    base_url = 'http://www.cgv.co.kr'

    uri = 'http://www.cgv.co.kr/search/?query='
    uri = uri + movie_name

    #print(uri)

    source_code = requests.get(uri)

    plain_text = source_code.text

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        #print(soup)

        redirect_list = soup.select('div.box-contents > a')

        if len(redirect_list) > 0:
            re_url = redirect_list[0]['href']
            print(base_url + re_url)

        source_code = requests.get(base_url + re_url)
        plain_text = source_code.text

        soup = BeautifulSoup(plain_text, 'lxml')

        point_list = soup.select('span.percent')

        if (len(point_list) > 0):
            point = float(point_list[0].get_text()[:-2])/100.0
            print(point)

    except Exception as e:
        raise e

    print("CGV SEARCH END")

cgv_search(sys.argv[0])
#-*- coding: euc-kr -*-

import sys
import requests
import lxml

from bs4 import BeautifulSoup
from cinema import cinema

def maxmovie_search(movie_name):

    movie_name = '범죄와의 전쟁 : 나쁜놈들 전성시대'
    name_utf = movie_name.encode('utf8')

    uri = 'http://search.maxmovie.com/search?sword='
    uri = uri + movie_name

    print(uri)

    source_code = requests.get(uri)

    plain_text = source_code.text

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        #print(soup)

        point_list = soup.select('span.sstar')

        if len(point_list) > 0:
            point = float(point_list[0].get_text())
            print(point)

    except Exception as e:
        raise e

    print("MAXMOVIE SEARCH END")

maxmovie_search(sys.argv[0])
#-*- coding: euc-kr -*-

import sys
import requests
import lxml

from bs4 import BeautifulSoup
from cinema import cinema
from selenium import webdriver

def watcha_search(movie_name):

    movie_name = '범죄와의 전쟁 : 나쁜놈들 전성시대'
    name_utf = movie_name.encode('utf8')

    uri = 'https://watcha.net/search/search?query='
    uri = uri + movie_name

    print(uri)

    source_code = requests.get(uri)

    plain_text = source_code.text

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        print(soup)

        redirect_list = soup.select('a.search.title.can_highlighted')

        if len(redirect_list) > 0:
            redirect = redirect_list[0].attrs('href')
            print(redirect)

    except Exception as e:
        raise e

    print("WATCHA SEARCH END")

watcha_search(sys.argv[0])
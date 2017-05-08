#-*- coding: euc-kr -*-

import sys
import requests
import lxml

from bs4 import BeautifulSoup
from selenium import webdriver

def daum_search(movie_name):

    driver = webdriver.Chrome(r'D:\Programs\Python36-32\Scripts\chromedriver.exe')
    driver.implicitly_wait(10)

    movie_name = '범죄와의 전쟁 : 나쁜놈들 전성시대'
    name_utf = movie_name.encode('utf8')

    uri = 'http://movie.daum.net/search/main?searchText='
    uri = uri + movie_name

    print(uri)

    #source_code = requests.get(uri)

    driver.get(uri)
    plain_text = driver.page_source

    #plain_text = source_code.text

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        #print(soup)

        point_list = soup.select('em.emph_grade')

        if len(point_list) > 0:
            point = float(point_list[0].get_text().strip())
            print(point)

    except Exception as e:
        raise e

    print("DAUM SEARCH END")

    return point

#daum_search(sys.argv[0])
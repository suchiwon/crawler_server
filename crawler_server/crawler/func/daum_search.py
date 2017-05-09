#-*- coding: euc-kr -*-

import sys
import requests
import lxml
import os

from bs4 import BeautifulSoup
from selenium import webdriver

base_path = os.path.dirname( os.path.abspath( __file__ ) )

def func_daum_search(movie_name):

    driver = webdriver.Chrome(base_path + '\\chromedriver.exe')
    driver.implicitly_wait(10)

    name_utf = movie_name.encode('utf8')

    uri = 'http://movie.daum.net/search/main?searchText='
    uri = uri + movie_name

    print(uri)

    #source_code = requests.get(uri)

    driver.get(uri)
    plain_text = driver.page_source

    point = 0

    #plain_text = source_code.text

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        #print(soup)

        point_list = soup.select('em.emph_grade')

        if len(point_list) > 0:
            point = point_list[0].get_text().strip()
            print(point)

    except Exception as e:
        raise e

    print("DAUM SEARCH END")

    return str(point)

#daum_search(sys.argv[0])
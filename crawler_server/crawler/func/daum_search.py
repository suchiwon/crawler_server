#-*- coding: euc-kr -*-

import sys
import requests
import lxml
import os
import json

import cinema

from bs4 import BeautifulSoup
from selenium import webdriver
from operator import methodcaller

base_path = os.path.dirname( os.path.abspath( __file__ ) )

def func_daum_search(movie_name):

    base_url = 'http://movie.daum.net'

    driver = webdriver.Chrome(base_path + '\\chromedriver.exe')
    driver.implicitly_wait(10)

    #name_utf = movie_name.encode('utf8')

    uri = 'http://movie.daum.net/search/main?searchText='
    uri = uri + movie_name

    print(uri)

    total_comment_list = []

    #source_code = requests.get(uri)

    driver.get(uri)
    plain_text = driver.page_source

    #plain_text = source_code.text

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        #print(soup)

        redirect_list = soup.select('a.link_join')

        if len(redirect_list) > 0:
            re_url = redirect_list[0]['href']
            print(base_url + re_url)

            driver.get(base_url + re_url)
            plain_text = driver.page_source

            soup = BeautifulSoup(plain_text, 'lxml')

            point_list = soup.select('em.emph_grade')
            profile_list = soup.select('em.link_profile')
            review_list = soup.select('p.desc_review')

            point = 0

            if len(point_list) > 0:
                point = point_list[0].get_text().strip()
                print(point)

            idx = 0

            while idx < len(profile_list):
                user_point = point_list[idx+2].get_text()
                profile = profile_list[idx].get_text()
                review = review_list[idx].get_text().strip()

                total_comment_list.append(cinema.Comment(profile, review, user_point))

                idx += 1

            commentsProvision = cinema.CommentsProvision(base_url + re_url, point, total_comment_list)

            json_list = json.dumps(commentsProvision, default=methodcaller("json"), ensure_ascii=False)
            print("DAUM SEARCH END")
            return json_list


    except Exception as e:
        raise e

    print("DAUM SEARCH FAILED")

#daum_search(sys.argv[0])
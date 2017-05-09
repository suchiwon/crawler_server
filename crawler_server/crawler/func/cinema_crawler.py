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

class Crawler:

    def __init__(self, base_url, follow_url, search_word):
        self.soup = ''
        self.base_url = base_url
        self.follow_url = follow_url
        self.search_word = search_word

    def getPullUrl(self):
        return self.base_url + self.follow_url + self.search_word

    def setSoup(self, url, is_use_driver):
        if is_use_driver == False:
            source_code = requests.get(url)

            plain_text = source_code.text
            self.soup = BeautifulSoup(plain_text, 'lxml')

        else:
            driver = webdriver.Chrome(base_path + '\\chromedriver.exe')
            driver.implicitly_wait(10)

            driver.get(url)
            plain_text = driver.page_source

            self.soup = BeautifulSoup(plain_text, 'lxml')

            driver.close()

        return self.soup

    def getSelector(self, tag):
        return self.soup.select(tag)

    def getRedirctUrl(self, tag, is_use_driver, is_use_base_url):
        self.setSoup(self.getPullUrl(), is_use_driver)

        redirect_list = self.soup.select(tag)

        if len(redirect_list) > 0:
            re_url = redirect_list[0]['href']

        if is_use_base_url == True:
            return self.base_url + re_url
        else:
            return re_url

    def makeJson(self, provision):
        return json.dumps(provision, default=methodcaller("json"), ensure_ascii=False)

    def makeCommentsProvision(self, url, soup, 
                              cinema_point_tag, user_id_tag, review_tag, user_point_tag, datetime_tag,
                              point_idx_offset, point_div):
        cinema_point_list = soup.select(cinema_point_tag)
        user_point_list = soup.select(user_point_tag)
        user_id_list = soup.select(user_id_tag)
        review_list = soup.select(review_tag)
        datetime_list = soup.select(datetime_tag)

        cinema_point = 0

        if len(cinema_point_list) > 0:
            cinema_point = float(cinema_point_list[0].get_text().strip())/point_div
            print(cinema_point)

        idx = 0

        total_comment_list = []

        while idx < len(user_id_list):
            user_point = user_point_list[idx + point_idx_offset].get_text()
            user_id = user_id_list[idx].get_text()
            review = review_list[idx].get_text().strip()
            datetime = datetime_list[idx].get_text().strip()

            total_comment_list.append(cinema.Comment(user_id, review, user_point, datetime))

            idx += 1

        commentsProvision = cinema.CommentsProvision(url, cinema_point, total_comment_list)

        return commentsProvision
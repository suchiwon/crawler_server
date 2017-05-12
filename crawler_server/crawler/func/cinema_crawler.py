"""
author: suchiwon
웹 페이지 crawling 기능 메소드 정의 클래스
다형성을 위해 정의하였으나 사이트마다 태그 처리 방식이 상이해 사용이 힘듬
"""

import sys
import requests
import lxml
import os
import json
import cinema

from bs4 import BeautifulSoup
from selenium import webdriver
from operator import methodcaller
from operator import eq
#from pyvirtualdisplay import Display

base_path = os.path.dirname( os.path.abspath( __file__ ) )

#crawling 기능 클래스
class Crawler:

    #생성자 메소드
    def __init__(self, base_url, follow_url, search_word):
        self.soup = ''
        self.base_url = base_url
        self.follow_url = follow_url
        self.search_word = search_word
        #self.display = Display(visible = 0, size=(800,600))

    #영화 정보 페이지 생성 메소드
    def getPullUrl(self):
        return self.base_url + self.follow_url + self.search_word

    #라이브러리를 사용해 페이지 crawling 결과 반환 메소드.
    #스크립트 사용 필요 여부에 따라 chromedriver 사용
    def setSoup(self, url, is_use_driver):

        if url.find('about:blank') >= 0:
            return None
        if is_use_driver == False:
            source_code = requests.get(url)

            plain_text = source_code.text
            self.soup = BeautifulSoup(plain_text, 'lxml')

        else:
            #self.display.start()
            driver = webdriver.Chrome(base_path + '\\chromedriver.exe')
            driver.implicitly_wait(10)

            driver.get(url)
            plain_text = driver.page_source

            self.soup = BeautifulSoup(plain_text, 'lxml')

            driver.quit()
            #self.display.stop()

        return self.soup

    #crawling 결과의 태그 요소 추출 메소드
    def getSelector(self, tag):
        return self.soup.select(tag)

    ###
    #영화 제목을 통해 검색을 하여 그 영화의 정보 페이지를 얻어오는 메소드
    #네이버 이외의 사이트에서 사용
    def getRedirctUrl(self, tag, title_tag, is_use_driver, is_use_base_url):
        self.setSoup(self.getPullUrl(), is_use_driver)

        #영화 검색 결과에서 영화 정보 페이지 url 리스트 추출
        redirect_list = self.soup.select(tag)
        title_list = self.soup.select(title_tag)

        #영화 검색 결과가 없을 시 전달할 빈 url 선언
        re_url = 'about:blank'

        #사이트 마다의 영화 제목의 표기가 달라 검색이 안되는 것을 방지하기 위해 제목 가공
        split_search_word = self.search_word.replace(' ','').split('(')[0].split(':')[0]

        #검색 결과에 선택한 영화와 같은 제목이 존재하면 같은 영화라고 판단해 url 저장
        if len(title_list) > 0:
            idx = 0
            while idx < len(title_list):
                split_title = title_list[idx].get_text().replace(' ','').split('(')[0].split(':')[0]
                if eq(split_search_word, split_title) == True:
                    re_url = redirect_list[idx].get('href')
                    break
                idx += 1

        #영화 정보 url 반환
        if is_use_base_url == True and re_url.find('about:blank') < 0:
            return self.base_url + re_url
        else:
            return re_url

    #정보 클래스를 JSON으로 가공하는 메소드
    def makeJson(self, provision):
        return json.dumps(provision, default=methodcaller("json"), ensure_ascii=False)

    #crawling 결과에서 태그에 맞는 요소 추출
    def getTagList(self, soup, tag):
        list = soup.get(tag)
        return list

    #영화 정보 클래스 생성. 각 사이트에서 요소에 맞는 태그를 받아서 추출해 저장 
    def makeCommentsProvision(self, site_type, url, soup, 
                              cinema_point_tag, user_id_tag, review_tag, user_point_tag, datetime_tag,
                              point_idx_offset, point_div):

        #영화의 정보 리스트 초기화
        cinema_point_list = []
        user_point_list = []
        user_id_list = []
        review_list = []
        datetime_list = []                                        
        
        #crawling 결과에서 요소의 값 추출
        if soup != None:
            cinema_point_list = soup.select(cinema_point_tag)
            user_point_list = soup.select(user_point_tag)
            user_id_list = soup.select(user_id_tag)
            review_list = soup.select(review_tag)
            datetime_list = soup.select(datetime_tag)

        #영화 검색 실패 값(-1)으로 초기화
        cinema_point = -1

        #영화 평점이 존재할 경우 평점을 가져옴
        if len(cinema_point_list) > 0:
            cinema_point = float(cinema_point_list[0].get_text().strip())/point_div
            print(cinema_point)

        idx = 0

        total_comment_list = []

        #댓글 리스트의 요소를 가져와 저장
        while idx < len(user_id_list):
            user_point = user_point_list[idx + point_idx_offset].get_text()
            user_id = user_id_list[idx].get_text()
            review = review_list[idx].get_text().strip()
            datetime = datetime_list[idx].get_text().strip()

            total_comment_list.append(cinema.Comment(user_id, review, user_point, datetime))

            idx += 1

        #영화 정보 클래스 생성 후 반환
        commentsProvision = cinema.CommentsProvision(site_type, url, cinema_point, total_comment_list)

        return commentsProvision
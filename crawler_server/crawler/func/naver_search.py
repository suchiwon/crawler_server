#-*- coding: utf-8 -*-

import sys
import requests
import lxml
import json

from bs4 import BeautifulSoup
import cinema
from operator import methodcaller

def func_naver_search(title, start_page, end_page):

    encode_bytes = title

    idx = 0

    encode_title = title
    #encode_title = ''

    #while idx < len(encode_bytes):
    #    hex_code = hex(encode_bytes[idx])
    #    encode_title += '%'
    #    encode_title += str(hex_code)[2:]
    #    idx += 1

    #print(encode_title)

    i = start_page
    title_list_saver = []

    total_title_list = []

    while True:
        uri = 'http://movie.naver.com/movie/search/result.nhn?section=movie&query='
     
        uri += encode_title

        uri += '&page='
        uri += str(i)

        print(uri)

        source_code = requests.get(uri)

        plain_text = source_code.text

        provision = cinema.CinemasProvision()

        #print(plain_text)

        try:
            soup = BeautifulSoup(plain_text, 'lxml')

            title_list = soup.select('ul.search_list_1 > li > dl > dt > a')
            point_list = soup.select('em.num')
            cuser_cnt_list = soup.select('em.cuser_cnt')
            etc_list = soup.select('dd.etc')
            image_url_list = soup.select('p.result_thumb > a > img')

            if title_list == title_list_saver:
                break

            idx = 0

            while idx < len(title_list):
                #title = link.string.split("<strong>")[1].split("</strong>")[0]
                title = title_list[idx].get_text()
                point = float(point_list[idx].get_text())
                cuser_cnt = int(cuser_cnt_list[idx].get_text()[4:-2])
                info = etc_list[2 * idx].get_text()
                actor_info = etc_list[2 * idx + 1].get_text()
                image_url = image_url_list[idx].get('src')


                if cuser_cnt > 0:
                    total_title_list.append(cinema.Cinema(title, point, cuser_cnt, info, actor_info, image_url))
                #print(title)

                idx = idx + 1

        except Exception as e:
            raise e

        i = i + 1

        if (i > end_page):
            break

        title_list_saver = title_list

    total_title_list.sort(reverse=True, key = cinema.Cinema.getKey)

    provision.Cinemas = total_title_list

    #for element in total_title_list:
    #    print(element.title + " " + str(element.point) + " " + str(element.cuser_cnt))

    json_list = json.dumps(provision, default=methodcaller("json"), ensure_ascii=False)
    print("NAVER SEARCH END")

    return json_list
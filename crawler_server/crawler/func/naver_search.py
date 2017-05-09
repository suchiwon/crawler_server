#-*- coding: utf-8 -*-

import cinema_crawler
import cinema

def func_naver_search(search_word, start_page, end_page):

    crawler_instance = cinema_crawler.Crawler('http://movie.naver.com/',
                                            'movie/search/result.nhn?section=movie&query=',
                                            search_word)

    page_idx = start_page
    title_list_saver = []
    total_title_list = []

    while True:

        uri = crawler_instance.getPullUrl()
        uri += '&page='
        uri += str(page_idx)
        print(uri)

        try:
            crawler_instance.setSoup(uri, False)

            title_list = crawler_instance.getSelector('ul.search_list_1 > li > dl > dt > a')
            point_list = crawler_instance.getSelector('em.num')
            cuser_cnt_list = crawler_instance.getSelector('em.cuser_cnt')
            etc_list = crawler_instance.getSelector('dd.etc')
            image_url_list = crawler_instance.getSelector('p.result_thumb > a > img')
            redirect_url_list = crawler_instance.getSelector('p.result_thumb > a')

            if title_list == title_list_saver:
                break

            idx = 0

            while idx < len(title_list):
                title = title_list[idx].get_text().split('(')[0]
                point = float(point_list[idx].get_text())
                cuser_cnt = int(cuser_cnt_list[idx].get_text()[4:-2])
                info = etc_list[2 * idx].get_text()
                actor_info = etc_list[2 * idx + 1].get_text()
                image_url = image_url_list[idx].get('src')
                redirect_url = redirect_url_list[idx].get('href')


                if cuser_cnt > 0:
                    total_title_list.append(cinema.Cinema(title, point, cuser_cnt, 
                                                          info, actor_info, image_url, redirect_url))

                idx = idx + 1

        except Exception as e:
            raise e

        page_idx += 1

        if (page_idx > end_page):
            break

        title_list_saver = title_list

    total_title_list.sort(reverse=True, key = cinema.Cinema.getKey)

    provision = cinema.CinemasProvision(total_title_list)

    #for element in total_title_list:
    #    print(element.title + " " + str(element.point) + " " + str(element.cuser_cnt))

    json_list = crawler_instance.makeJson(provision)
    print("NAVER SEARCH END")

    return json_list
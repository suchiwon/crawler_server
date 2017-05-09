#-*- coding: utf-8 -*-

import cinema_crawler
import cinema

def func_naver_search(search_word, start_page, end_page):

    encode_byte = str(bytes(search_word,'euc-kr'))

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
                code = int(str(redirect_url_list[idx].get('href'))[-5:])


                if cuser_cnt > 0:
                    total_title_list.append(cinema.Cinema(title, point, cuser_cnt, 
                                                          info, actor_info, image_url, code))

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

def func_naver_search_one_cinema(redirect_code):
    crawler_instance = cinema_crawler.Crawler('http://movie.naver.com/',
                                            'movie/search/result.nhn?section=movie&query=',
                                            '')
    redirect_url = 'http://movie.naver.com/movie/bi/mi/basic.nhn?code=' + str(redirect_code)
    try:
        soup = crawler_instance.setSoup(redirect_url, False)

        #provision = crawler_instance.makeCommentsProvision(redirect_url, soup, 'div.star_score > em', 'div.score_reple > dl > dt > em',
        #                                                   'div.score_reple > p',
        #                                                   'div.star_score > em','div.score_reple > dl > dt > em', 2, 1)

        cinema_point_list = soup.select('div.star_score > em')
        user_point_list = soup.select('div.star_score > em')
        user_id_list = soup.select('div.score_reple > dl > dt > em > a > span')
        review_list = soup.select('div.score_reple > p')
        datetime_list = soup.select('div.score_reple > dl > dt > em')

        cinema_point = 0

        if len(cinema_point_list) > 0:
            cinema_point = float(cinema_point_list[8].get_text().strip())
            print(cinema_point)

        idx = 0

        total_comment_list = []

        while idx < len(user_id_list):
            user_point = user_point_list[idx + 10].get_text()
            user_id = user_id_list[idx].get_text().strip()
            review = review_list[idx].get_text().strip()
            datetime = datetime_list[idx * 2 + 1].get_text().strip()

            total_comment_list.append(cinema.Comment(user_id, review, user_point, datetime))

            idx += 1

        commentsProvision = cinema.CommentsProvision('naver', redirect_url, cinema_point, total_comment_list)
                                            
        json_list = crawler_instance.makeJson(commentsProvision)
        print("NAVER SEARCH END")
        return json_list

    except Exception as e:
        raise e

    print("NAVER SEARCH FAILED")

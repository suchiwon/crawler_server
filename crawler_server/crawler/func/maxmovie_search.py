#-*- coding: euc-kr -*-

import cinema_crawler
import cinema

def func_maxmovie_search(movie_name):

    crawler_instance = cinema_crawler.Crawler('http://search.maxmovie.com',
                                              '/search?sword=',
                                              movie_name)

    print(crawler_instance.getPullUrl())

    try:
        redirect_url = crawler_instance.getRedirctUrl('p.sage > a', False, False)

        soup = crawler_instance.setSoup(redirect_url, True)

        #print(soup)

        #provision = crawler_instance.makeCommentsProvision(redirect_url, soup, 'div.myDetailTex_point > font.font_rdB b',
        #                                                   'div#content-center > table > tbody > tr > td > font',
        #                                                   'div#content-center > table > tbody > tr > td > a > font:not(.font_or)',
        #                                                   'div#content-center > table > tbody > tr > td > a > font.font_or'
        #                                                   ,'div#content-center > table > tbody > tr > td.font_br.s',
        #                                                   0, 1)
        
        
        cinema_point_list = soup.select('div.myDetailTxt_point > font.font_rdB.b')
        user_point_list = soup.select('div#content-center > table > tbody > tr > td > a > font.font_or')
        user_id_list = soup.select('div#content-center > table > tbody > tr > td > font')
        review_list = soup.select('div#content-center > table > tbody > tr > td > a > font')
        datetime_list = soup.select('div#content-center > table > tbody > tr > td.font_br.s')

        cinema_point = 0

        if len(cinema_point_list) > 0:
            cinema_point = float(cinema_point_list[0].get_text().strip())
            print(cinema_point)

        idx = 0

        total_comment_list = []

        while idx < len(user_id_list):
            user_point = user_point_list[idx].get_text()
            user_id = user_id_list[idx].get_text()
            review = review_list[idx * 2 + 1].get_text().strip()
            datetime = datetime_list[idx].get_text().strip()

            total_comment_list.append(cinema.Comment(user_id, review, user_point, datetime))

            idx += 1

        commentsProvision = cinema.CommentsProvision('maxmovie', redirect_url, cinema_point, total_comment_list)
                                    
        json_list = crawler_instance.makeJson(commentsProvision)
        print("MAXMOVIE SEARCH END")
        return json_list

    except Exception as e:
        raise e

    print("MAXMOVIE SEARCH FAILED")
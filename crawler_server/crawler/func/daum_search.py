#-*- coding: euc-kr -*-

"""
author: suchiwon
다음 영화 사이트를 crawling 하는 메소드를 정의.
한 영화의 정보를 얻는 메소드 존재.
"""

import cinema_crawler
import cinema
from operator import methodcaller

"""
author: suchiwon
다음 사이트의 특정 영화의 정보 결과를 얻어오는 메소드
JSONObject 형식으로 반환
반환 JSONObject 형식:
{"site_type":"영화 사이트 종류","url":"사이트의 url","point":"영화의 사이트에서의 평점","comments":[댓글 JSONArrary]}
"""
def func_daum_search(movie_name):

    crawler_instance = cinema_crawler.Crawler('http://movie.daum.net',
                                              '/search/main?searchText=',
                                              movie_name)

    #print(crawler_instance.getPullUrl())

    try:
        redirect_url = crawler_instance.getRedirctUrl('a.link_join', 'strong.tit_join', True, True)

        soup = crawler_instance.setSoup(redirect_url, True)

        commentsProvision = crawler_instance.makeCommentsProvision('daum', redirect_url, soup, 'em.emph_grade', 'em.link_profile', 'p.desc_review',
                                                           'em.emph_grade','span.info_append', 2, 1)
                                    
        json_list = crawler_instance.makeJson(commentsProvision)
        print("DAUM SEARCH END")
        return json_list       

    except Exception as e:
        raise e

    print("DAUM SEARCH FAILED")

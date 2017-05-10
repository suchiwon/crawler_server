#-*- coding: euc-kr -*-

import cinema_crawler
import cinema
from operator import methodcaller

def func_daum_search(movie_name):

    crawler_instance = cinema_crawler.Crawler('http://movie.daum.net',
                                              '/search/main?searchText=',
                                              movie_name)

    print(crawler_instance.getPullUrl())

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

#-*- coding: euc-kr -*-

import cinema_crawler
import cinema

def func_maxmovie_search(movie_name):

    crawler_instance = cinema_crawler.Crawler('http://search.maxmovie.com',
                                              '/search?sword=',
                                              movie_name)

    print(crawler_instance.getPullUrl())

    try:
        redirect_url = crawler_instance.getRedirctUrl('p.sage > a.ag_4', False, False)

        soup = crawler_instance.setSoup(redirect_url, False)

        provision = crawler_instance.makeCommentsProvision(redirect_url, soup, 'div.myDetailTex_point > font.font_rdB.b',
                                                           'div#content-center > table . tbody > tr > td > font',
                                                           'div#content-center > table . tbody > tr > td > a > font',
                                                           'div#content-center > table . tbody > tr > td > a > font.font_or'
                                                           ,'div#content-center > table . tbody > tr > td.font_br.s',
                                                           2, 1)
                                    
        json_list = crawler_instance.makeJson(provision)
        print("MAXMOVIE SEARCH END")
        return json_list


    except Exception as e:
        raise e

    print("MAXMOVIE SEARCH FAILED")
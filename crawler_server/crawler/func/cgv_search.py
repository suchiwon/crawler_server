#-*- coding: euc-kr -*-

import cinema_crawler
import cinema

def func_cgv_search(movie_name):

    crawler_instance = cinema_crawler.Crawler('http://www.cgv.co.kr',
                                              '/search/?query=',
                                              movie_name)

    print(crawler_instance.getPullUrl())

    try:
        redirect_url = crawler_instance.getRedirctUrl('div.box-contents > a', False, True)

        soup = crawler_instance.setSoup(redirect_url, True)

        print(soup)
        
        cinema_point_list = soup.select('span.percent')
        user_id_list = soup.select('a.commentMore')
        review_list = soup.select('div.box-comment > p')
        datetime_list = soup.select('span.day')

        cinema_point = 0

        if len(cinema_point_list) > 0:
            cinema_point = float(cinema_point_list[0].get_text().strip()[:-1])/10
            print(cinema_point)

        idx = 0

        total_comment_list = []

        while idx < len(user_id_list):
            user_id = user_id_list[idx].get_text()
            review = review_list[idx].get_text().strip()
            datetime = datetime_list[idx].get_text().strip()

            total_comment_list.append(cinema.Comment(user_id, review, 0, datetime))

            idx += 1

        commentsProvision = cinema.CommentsProvision('cgv', redirect_url, cinema_point, total_comment_list)
                                    
        json_list = crawler_instance.makeJson(commentsProvision)
        print("MAXMOVIE SEARCH END")
        return json_list


    except Exception as e:
        raise e

    print("MAXMOVIE SEARCH FAILED")

#cgv_search(sys.argv[0])
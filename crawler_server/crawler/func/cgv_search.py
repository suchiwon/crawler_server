#-*- coding: euc-kr -*-

import cinema_crawler
import cinema

def func_cgv_search(movie_name):

    name_utf = movie_name.encode('utf8')

    base_url = 'http://www.cgv.co.kr'

    uri = 'http://www.cgv.co.kr/search/?query='
    uri = uri + movie_name

    #print(uri)

    source_code = requests.get(uri)

    plain_text = source_code.text

    point = 0

    try:
        soup = BeautifulSoup(plain_text, 'lxml')

        #print(soup)

        redirect_list = soup.select('div.box-contents > a')

        if len(redirect_list) > 0:
            re_url = redirect_list[0]['href']
            print(base_url + re_url)

        source_code = requests.get(base_url + re_url)
        plain_text = source_code.text

        soup = BeautifulSoup(plain_text, 'lxml')

        point_list = soup.select('span.percent')

        if (len(point_list) > 0):
            point = float(point_list[0].get_text()[:-2])/10.0
            print(point)

    except Exception as e:
        raise e

    print("CGV SEARCH END")

    return point

#cgv_search(sys.argv[0])
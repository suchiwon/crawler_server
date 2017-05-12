import json

"""
author: suchiwon
영화의 정보와 댓글 하나를 JSONObject로 나타내기 위한 클래스와
이 클래스를 리스트로 묶어 하나의 JSONObject로 만들기 위한 클래스를 정의
"""

"""
author: suchiwon
JSONObject로의 변환을 위한 클래스
"""
class JSONEncodable(object):
    def json(self):
        return vars(self)

"""
author: suchiwon
네이버 사이트에서 검색한 영화 목록에서의 한 영화의 정보 저장 클래스
"""
class Cinema(JSONEncodable):
    
    #생성자 메소드
    def __init__(self, title, point, cuser_cnt, info, actor_info, image_url, code):
        self.title = title
        self.point = point
        self.cuser_cnt = cuser_cnt
        self.info = info
        self.actor_info = actor_info
        self.image_url = image_url
        self.code = code

    #자기 참조 메소드
    def __repr__(self):
        return '{}: {} {} {} {} {} {} {}'.format(self.__class__.__name__,
                                                    self.title,
                                                    self.point,
                                                    self.cuser_cnt,
                                                    self.info,
                                                    self.actor_info,
                                                    self.image_url,
                                                    self.code)
    #비교 메소드. 평가 유저 수를 오름차순으로 비교
    def __cmp__(self, other):
        if hasattr(other, 'cuser_cnt'):
            return self.cuser_cnt.__cmp__(other.cuser_cnt)
    
    #비교 메소드에서 사용할 유저 수 반환 메소드
    def getKey(self):
        return self.cuser_cnt

"""
author: suchiwon
영화 목록을 저장해 JSONObject로 만들기 위한 클래스
"""
class CinemasProvision(JSONEncodable):
    def __init__(self, total_cinema_list):
        self.ID = None
        self.Type = None
        self.Cinemas = total_cinema_list

"""
author: suchiwon
특정 영화의 한 댓글 정보를 저장하는 클래스
"""
class Comment(JSONEncodable):
    
    #생성자 메소드
    def __init__(self, user_id, comment, point, datetime):
        self.user_id = user_id
        self.comment = comment
        self.point = point
        self.datetime = datetime

    #자기 참조 메소드
    def __repr__(self):
        return '{}: {} {} {} {}'.format(self.__class__.__name__,
                                        self.user_id,
                                        self.comment,
                                        self.point,
                                        self.datetime)

"""
author: suchiwon
영화의 댓글 리스트, 평점, url을 저장해 JSONObject로 만들기 위한 클래스
"""
class CommentsProvision(JSONEncodable):
    def __init__(self, site_type, url, point, comments):
        self.site_type = site_type
        self.url =  url
        self.point = point
        self.comments = comments                          
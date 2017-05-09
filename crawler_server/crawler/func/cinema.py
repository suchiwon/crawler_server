import json

class JSONEncodable(object):
    def json(self):
        return vars(self)

class Cinema(JSONEncodable):
    """영화의 정보 저장 클래스"""
    def __init__(self, title, point, cuser_cnt, info, actor_info, image_url, redirect_url):
        self.title = title
        self.point = point
        self.cuser_cnt = cuser_cnt
        self.info = info
        self.actor_info = actor_info
        self.image_url = image_url
        self.redirect_url = redirect_url

    def __repr__(self):
        return '{}: {} {} {} {} {} {} {}'.format(self.__class__.__name__,
                                                    self.title,
                                                    self.point,
                                                    self.cuser_cnt,
                                                    self.info,
                                                    self.actor_info,
                                                    self.image_url,
                                                    self.redirect_url)

    def __cmp__(self, other):
        if hasattr(other, 'cuser_cnt'):
            return self.cuser_cnt.__cmp__(other.cuser_cnt)

    def getKey(self):
        return self.cuser_cnt

class CinemasProvision(JSONEncodable):
    def __init__(self, total_cinema_list):
        self.ID = None
        self.Type = None
        self.Cinemas = total_cinema_list

class Comment(JSONEncodable):
    """영화의 댓글 정보 클래스"""
    def __init__(self, user_id, comment, point, datetime):
        self.user_id = user_id
        self.comment = comment
        self.point = point
        self.datetime = datetime

    def __repr__(self):
        return '{}: {} {} {} {}'.format(self.__class__.__name__,
                                        self.user_id,
                                        self.comment,
                                        self.point,
                                        self.datetime)

class CommentsProvision(JSONEncodable):
    def __init__(self, url, point, comments):
        self.url =  url
        self.point = point
        self.comments = comments                          
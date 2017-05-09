import json

class JSONEncodable(object):
    def json(self):
        return vars(self)

class Cinema(JSONEncodable):
    """영화의 정보 저장 클래스"""
    def __init__(self, title, point, cuser_cnt, info, actor_info, image_url):
        self.title = title
        self.point = point
        self.cuser_cnt = cuser_cnt
        self.info = info
        self.actor_info = actor_info
        self.image_url = image_url

    def __repr__(self):
        return '{}: {} {} {} {} {} {}'.format(self.__class__.__name__,
                                                self.title,
                                                self.point,
                                                self.cuser_cnt,
                                                self.info,
                                                self.actor_info,
                                                self.image_url)

    def __cmp__(self, other):
        if hasattr(other, 'cuser_cnt'):
            return self.cuser_cnt.__cmp__(other.cuser_cnt)

    def getKey(self):
        return self.cuser_cnt

class CinemasProvision(JSONEncodable):
    def __init__(self):
        self.ID = None
        self.Type = None
        self.Cinemas = []

class Comment(JSONEncodable):
    """영화의 댓글 정보 클래스"""
    def __init__(self, user_id, comment, point):
        self.user_id = user_id
        self.comment = comment
        self.point = point

    def __repr__(self):
        return '{}: {} {} {}'.format(self.__class__.__name__,
                                        self.user_id,
                                        self.comment,
                                        self.point)

class CommentsProvision(JSONEncodable):
    def __init__(self, url, point, comments):
        self.url =  url
        self.point = point
        self.comments = comments                          
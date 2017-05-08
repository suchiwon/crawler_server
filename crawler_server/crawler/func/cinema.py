import json

class JSONEncodable(object):
    def json(self):
        return vars(self)

class Cinema(JSONEncodable):
    """영화의 정보 저장 클래스"""
    def __init__(self, title, point, cuser_cnt):
        self.title = title
        self.point = point
        self.cuser_cnt = cuser_cnt

    def __repr__(self):
        return '{}: {} {} {}'.format(self.__class__.__name__,
                                    self.title,
                                    self.point,
                                    self.cuser_cnt)

    def __cmp__(self, other):
        if hasattr(other, 'cuser_cnt'):
            return self.cuser_cnt.__cmp__(other.cuser_cnt)

    def getKey(self):
        return self.cuser_cnt

class Provision(JSONEncodable):
    def __init__(self):
        self.ID = None
        self.Type = None
        self.Cinemas = []

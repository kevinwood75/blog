import uuid
from common.database import Database
from models.blog import Blog
from flask import session
import datetime


class User(object):
    def __init__(self, email, date, hits, ab, runs, second, third, hr, rbi, so, _id=None):
        self.email = email
        self.date = date
        self.hits = hits
        self.ab = ab
        self.runs = runs
        self.second = second
        self.third = third
        self.hr = hr
        self.rbi = rbi
        self.so = so
        self._id = uuid.uuid4().hex if _id is None else _id
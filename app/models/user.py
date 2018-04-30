import datetime
import uuid

from flask import session

from app.common.database import Database
from app.models.blog import Blog


class User(object):
    def __init__(self, email, password, player, age, sport, team,  _id=None):
        self.email = email
        self.password = password
        self.player = player
        self.age = age
        self.sport = sport
        self.team = team
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # User.login_valid("kevin.wood75@gmail.com", "12345")
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password, player, age, sport, team):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password, player, age, sport, team)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        # title, content, date=datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password,
            "player": self.player,
            "age": self.age,
            "sport": self.sport,
            "team": self.team
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
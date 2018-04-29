import uuid

from app.common.database import Database


class Baseball(object):
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

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "date": self.date,
            "hits": self.hits,
            "ab": self.ab,
            "runs": self.runs,
            "second": self.second,
            "third": self.third,
            "hr": self.hr,
            "rbi": self.rbi,
            "so": self.so
        }

    @classmethod
    def input(cls, email, date, hits, ab, runs, second, third, hr, rbi, so):
        new_stats = cls(email, date, check_null(hits), check_null(ab), check_null(runs),
                        check_null(second), check_null(third), check_null(hr),
                        check_null(rbi), check_null(so))
        new_stats.save_to_mongo()

    def save_to_mongo(self):
        Database.insert("baseball", self.json())

    @staticmethod
    def from_blog(email):
        return [stats for stats in Database.find(collection='baseball', query={'email': email})]

    @classmethod
    def get_by_date(cls, date):
        data = Database.find_one("baseball", {"date": date})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_user(cls, date, email):
        data = Database.find_one("baseball", {"date": date, "email": email})
        if data is not None:
            return cls(**data)

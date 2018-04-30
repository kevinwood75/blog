import uuid

from app.common.database import Database

class Roster(object):
    def __init__(self, number, firstname, lastname, bathand, fieldhand, birthyear, _id = None):
        self.number = number
        self.firstname = firstname
        self.lastname = lastname
        self.bathand = bathand
        self.fieldhand = fieldhand
        self.birthyear = birthyear
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "number": self.number,
            "_id": self._id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "bathand": self.bathand,
            "fieldhand": self.fieldhand,
            "birthyear": self.birthyear
        }

    @classmethod
    def input(cls, number, firstname, lastname, bathand, fieldhand, birthyear):
        new_stats = cls(number, firstname, lastname, bathand, fieldhand, birthyear)
        new_stats.save_to_mongo()


    @classmethod
    def get_by_number(cls, number):
        existing_id = Database.find_one_field("roster", {"number": number}, {"_id": 1})
        return cls(**existing_id)

    def save_to_mongo(self):
        Database.insert("roster", self.json())
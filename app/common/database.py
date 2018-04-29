import pymongo

class Database(object):
    URI = "mongodb://192.168.2.148:27017"
#  URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def update(collection, data, query):
        Database.DATABASE[collection].update(query, data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_one_field(collection, query, field):
        return Database.DATABASE[collection].find_one(query, field)
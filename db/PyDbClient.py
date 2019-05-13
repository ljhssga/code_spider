import pymongo


class PyDB():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://111.231.137.74:27017/")
        self.db = self.client["spider"]
        self.col = self.db["names"]

    def delete_one(self,data):
        self.col.delete_one(data)

    def find_all(self):
        return self.col.find()
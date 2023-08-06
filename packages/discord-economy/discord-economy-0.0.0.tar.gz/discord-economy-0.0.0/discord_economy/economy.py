import pymongo
import discord

class Client:
    def __init__(self, *, db='discord_economy',db_cluster='Economy', mongo_datebase='localhost:27017'):
        self._name = db_cluster
        self._db = db
        self._mongo_connection = pymongo.MongoClient(mongo_datebase)

    def work(self, cash:int, user_id: discord.User):
        db = self._mongo_connection[self._db][self._name]
        doc = db.find_one({"_id": user_id})
        if not doc:
            db.insert_one({"_id": user_id, 
                "Eco": {'cash': cash, 'bank': 0}})
            return "Made an account."

        if not "Eco" in doc:
            db.find_one_and_update({"_id": user_id}, {"$set": {
                "Eco": {'cash': cash, 'bank': 0},
      
                }})
            return
        money = doc['Eco']['cash']
        db.find_one_and_update({"_id": user_id}, {"$set": {
            "Eco": {'cash': money + cash, 'bank': 0},

        }})
    
    def deposit(self, amount: int, user_id: discord.User):
        db = self._mongo_connection[self._db][self._name]
        doc = db.find_one({"_id": user_id})


        if not doc:
            db.insert_one({"_id": user_id,
                           "Eco": {'cash': 0, 'bank': 0}})
            doc = db.find_one({"_id": user_id})

        if not "Eco" in doc:
            db.find_one_and_update({"_id": user_id}, {"$set": {
                "Eco": {'cash': 0, 'bank': 0},

            }})
            doc = db.find_one({"_id": user_id})
        if (amount > doc['Eco']['cash'] or doc['Eco']['cash']==0):
            return False
        money = doc['Eco']['bank']
        db.find_one_and_update({"_id": user_id}, {"$set": {
            "Eco": {'cash': 0, 'bank': money + amount},

        }})

    def withdraw(self, amount: int, user_id: discord.User):
        db = self._mongo_connection[self._db][self._name]
        doc = db.find_one({"_id": user_id})


        if not doc:
            db.insert_one({"_id": user_id,
                           "Eco": {'cash': 0, 'bank': 0}})
            doc = db.find_one({"_id": user_id})

        if not "Eco" in doc:
            db.find_one_and_update({"_id": user_id}, {"$set": {
                "Eco": {'cash': 0, 'bank': 0},

            }})
            doc = db.find_one({"_id": user_id})
        if (amount > doc['Eco']['bank'] or doc['Eco']['bank']==0):
            return False
        money = doc['Eco']['cash']
        db.find_one_and_update({"_id": user_id}, {"$set": {
            "Eco": {'cash': money + amount, 'bank': 0},

        }})
    def get_cash(self, user_id: discord.User):
        db = self._mongo_connection[self._db][self._name]
        doc = db.find_one({"_id": user_id})
        if not doc:
            return False

        return doc['Eco']['cash']
    def get_bank(self, user_id: discord.User):
        db = self._mongo_connection[self._db][self._name]
        doc = db.find_one({"_id": user_id})
        if not doc:
            return False

        return doc['Eco']['bank']

    def get_network(self, user_id: discord.User):
        db = self._mongo_connection[self._db][self._name]
        doc = db.find_one({"_id": user_id})
        if not doc:
            return False
        return doc["Eco"]['cash'] + doc['Eco']['bank']
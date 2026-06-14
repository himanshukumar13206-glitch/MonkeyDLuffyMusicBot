from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

class DatabaseManager:
    @staticmethod
    def add_user(user_id, username):
        if not db.users.find_one({"_id": user_id}):
            db.users.insert_one({"_id": user_id, "username": username, "requests": 0})

    @staticmethod
    def get_user_stats():
        return db.users.count_documents({})

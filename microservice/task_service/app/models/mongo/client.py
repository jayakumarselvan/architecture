import os
import pymongo
from dotenv import load_dotenv

load_dotenv()


class MongoClient:
    def __init__(self):
        self.MONGO_HOST = os.getenv("MONGO_HOST")
        self.MONGO_PORT = os.getenv("MONGO_PORT")
        self.connection_string = f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"

    def get_connection(self):
        try:
            client = pymongo.MongoClient(self.connection_string, serverSelectionTimeoutMS=20000)
            return client
        except pymongo.errors.ConnectionFailure as e:
            print(e)
            raise

import os
from bson.objectid import ObjectId

from app.models.mongo.client import MongoClient


class TaskModel:
    def __init__(self):
        mongo_client_service = MongoClient()
        self.mongo_client = mongo_client_service.get_connection()
        self.mongodb_user_schema = os.getenv("MONGODB_TASK_SCHEMA")
        self.db = self.mongo_client[self.mongodb_user_schema]
        self.collection_task = self.db.get_collection("tasks")

    @staticmethod
    def serialize_document(document):
        """ Convert MongoDB document to serializable format """
        if '_id' in document:
            document['_id'] = str(document['_id'])
        return document

    def get_task_by_id(self, task_id):
        query = {"_id": ObjectId(task_id)}
        task = self.collection_task.find_one(query)
        return task

    def update_task_by_id(self, task_data, task_id):
        result = self.collection_task.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": task_data}
        )
        return result

    def add_task(self, task_data):
        result = self.collection_task.insert_one(task_data)
        return result

    def list_task(self, skip, limit):
        task_cursor = self.collection_task.find().skip(skip).limit(limit)
        result = [self.serialize_document(doc) for doc in task_cursor]
        return result

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            # User found, proceed to delete
            result = self.collection_task.delete_one({"_id": ObjectId(task_id)})
            return result
        else:
            return None

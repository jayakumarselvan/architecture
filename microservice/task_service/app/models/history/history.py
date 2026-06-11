import os

from app.helpers.common import get_current_timestamp_iso_format
from app.models.mongo.client import MongoClient


class HistoryModel:
    def __init__(self):
        self.mongodb_aisummarization_schema = os.getenv("MONGODB_TASK_SCHEMA")
        mongo_client_service = MongoClient()
        self.mongo_client = mongo_client_service.get_connection()
        self.db = self.mongo_client[self.mongodb_aisummarization_schema]
        self.collection_name_tasks_history = "tasks_history"
        self.module_type_tasks = 'TASKS'

    def get_tasks_history_collection(self):
        return self.db.get_collection(self.collection_name_tasks_history)

    def add_history(self, module_type, action, data, created_by):
        created_at = get_current_timestamp_iso_format()

        history_data = {
            "action": action,
            "historyCreatedBy": created_by,
            "historyCreatedAt": created_at,
            "data": data,
        }

        if module_type == self.module_type_tasks:
            history_data["TaskId"] = str(data["_id"])
            collection_tasks_history = self.get_tasks_history_collection()
            collection_tasks_history.insert_one(history_data)

        return history_data

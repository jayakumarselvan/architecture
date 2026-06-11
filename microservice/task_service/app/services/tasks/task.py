import os

from app.core.external_api import query_api, construct_url
from app.helpers.common import get_current_timestamp_iso_format
from app.helpers.task import add_assigned_user_name
from app.models.history.history import HistoryModel
from app.models.tasks.task_model import TaskModel


class TaskService:
    def __init__(self):
        self.task_model = TaskModel()
        self.history_model = HistoryModel()
        self.action_create = "CREATE"
        self.action_update = "UPDATE"
        self.action_patch_update = "PATCH-UPDATE"
        self.user_management_api_host = os.getenv("USER_MANAGEMENT_API_HOST")
        self.user_management_api_port = os.getenv("USER_MANAGEMENT_API_PORT")
        self.user_management_api_base_path = os.getenv("USER_MANAGEMENT_API_BASE_PATH")
        self.user_management_api_list_path_param = os.getenv("USER_MANAGEMENT_API_LIST_PATH_PARAM")

    def add_or_update(self, task_data, task_id, requester_id):
        task_data["updatedBy"] = requester_id
        task_data["updatedAt"] = get_current_timestamp_iso_format()

        if task_id:
            # Update an existing user details
            result = self.task_model.update_task_by_id(task_data, task_id)
            if result.matched_count == 0:
                return {
                    "status": False,
                    "statusCode": 404,
                    "message": "Task not found!",
                    "data": {}
                }
            history_data = task_data.copy()
            history_data["_id"] = task_id
            self.history_model.add_history(self.history_model.module_type_tasks, self.action_update, history_data,
                                           requester_id)
            return {
                "status": True,
                "statusCode": 200,
                "message": "Task updated successfully",
                "data": {"id": task_id}
            }
        else:
            # Add a task
            task_data["createdBy"] = requester_id
            task_data["createdAt"] = get_current_timestamp_iso_format()

            new_task = self.task_model.add_task(task_data)
            history_data = task_data.copy()
            history_data["_id"] = new_task.inserted_id
            self.history_model.add_history(self.history_model.module_type_tasks, self.action_create, history_data,
                                           requester_id)
            return {"status": True,
                    "statusCode": 200,
                    "message": "Task added successfully",
                    "data": {"id": str(new_task.inserted_id)}
                    }

    def list_task(self, skip, limit):
        query_params = {"skip": 0, "limit": 10}
        task_details = self.task_model.list_task(skip, limit)
        url = construct_url(self.user_management_api_host, self.user_management_api_port,
                            self.user_management_api_base_path, "list", query_params)
        user_details = query_api(url)
        result = add_assigned_user_name(task_details, user_details)
        return result

    def patch_update(self, task_id, task_data, requester_id):
        task_data = self.validate_task_data(task_data)
        result = self.task_model.update_task_by_id(task_data, task_id)
        if result.matched_count == 0:
            return {
                "status": False,
                "statusCode": 404,
                "message": "Task not found",
                "data": {}
            }
        data = self.task_model.get_task_by_id(task_id)
        self.history_model.add_history(self.history_model.module_type_tasks, self.action_patch_update, data,
                                       requester_id)
        return {
            "status": True,
            "statusCode": 200,
            "message": "Task updated successfully",
            "data": {"id": task_id}
        }

    def delete_task(self, task_id):
        result = self.task_model.delete_task(task_id)
        if result:
            if result.deleted_count == 1:
                return {"status": True,
                        "statusCode": 200,
                        "message": "Task deleted successfully",
                        }
            return {"status": False,
                    "statusCode": 404,
                    "message": "Failed to delete task",
                    }

        else:
            return {"status": False,
                    "statusCode": 404,
                    "message": "Task not found",
                    }

    @staticmethod
    def validate_task_data(task_data):
        allowed_values = {
            "priority": {"LOW", "MEDIUM", "HIGH"},
            "status": {"TODO", "IN PROGRESS", "DONE"},
            "assignedUserId": None
        }

        validated_data = {
            key: value
            for key, value in task_data.items()
            if key in allowed_values and (allowed_values[key] is None or value in allowed_values[key])
        }

        return validated_data

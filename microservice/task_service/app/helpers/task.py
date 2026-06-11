def add_assigned_user_name(task_details, user_details):
    user_lookup = {user["_id"]: f"{user['username']} {user['email']}" for user in user_details}
    # Update task_details with the assignedUserName field
    for item in task_details:
        assigned_user_id = item.get("assignedUserId")
        if assigned_user_id in user_lookup:
            item["assignedUserName"] = user_lookup[assigned_user_id]
        else:
            item["assignedUserName"] = "-"
    return task_details

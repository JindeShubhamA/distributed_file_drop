import uuid
import time
import json
from src.file_uploader import index_cache
# import index_cache


class FileUploader:
    def __init__(self, file_cache, file_queue_manager, user_queue_manager, admin_queue_manager, index_cache):
        self.file_cache = file_cache
        self.file_queue_manager = file_queue_manager
        self.user_queue_manager = user_queue_manager
        self.admin_queue_manager = admin_queue_manager
        self.index_cache = index_cache

    def send_file_for_upload(self, file_path, user_id, user_name):
        file_name = str(uuid.uuid4())

        result = self.file_cache.store(file_path, file_name)
        if not result["success"]:
            result["error_msg"] = "Error while storing the file contents in cache : " + result["error"]
            return result

        file_cache_key = result["file_key"]

        result = self.index_cache.create(file_name)
        if not result["success"]:
            result["error_msg"] = "Error while creating file index on the cache : " + result["error"]
            return result

        result = self.__publish_file_upload_queue_event(
            file_name, file_cache_key, user_id, user_name)
        if not result["message_published"]:
            result["success"] = False
            result["error_msg"] = result["error"]
            return result

        return {"success": True,
                "file_name": file_name}

    def delete_uploaded_file(self, file_name, user_id, user_name):
        result = self.file_cache.delete(file_name)
        if not result["success"]:
            result["error_msg"] = "Error while deleting the file from cache : " + \
                result["error"]
            return result

        result = self.index_cache.update(
            file_name, index_cache.STATUS_FILE_UPLOADED)
        if not result["success"]:
            result["error_msg"] = "Error while updating file status in index cache  : " + \
                result["error"]
            return result

        result = self.__publish_client_notification_queue_event(
            file_name, user_id, user_name)
        if not result["message_published"]:
            result["success"] = False
            return result

        return {"success": True}

    def __publish_file_upload_queue_event(self, file_name, file_key, user_id, user_name):
        msg = {"id": str(uuid.uuid4()),
               "file_name": file_name,
               "file_cache_key": file_key,
               "user_id": user_id,
               "user_name": user_name,
               "event_timestamp": time.time()}

        msg_json = json.dumps(msg)
        return self.file_queue_manager.publish(msg_json)

    def __publish_client_notification_queue_event(self, file_name, user_id, user_name):
        msg = {"id": str(uuid.uuid4()),
               "file_name": file_name,
               "user_id": user_id,
               "user_name": user_name,
               "event_timestamp": time.time()}

        msg_json = json.dumps(msg)
        result = self.user_queue_manager.publish(msg_json)
        if not result["message_published"]:
            result["error_msg"] = "Error while publishing message to user notification queue : " + result["error"]
            return result

        result = self.admin_queue_manager.publish(msg_json)
        if not result["message_published"]:
            result["error_msg"] = "Error while publishing message to admin notification queue : " + result["error"]
            return result

        return result
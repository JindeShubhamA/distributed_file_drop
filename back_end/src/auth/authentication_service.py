import uuid
from . import user_db

ERROR_UNAUTHORISED_REQUEST = "User not authorised to fetch this resource"


class Authenticator:
    def __init__(self, db_config):
        self.db = user_db.UserDB(db_config)

    def create_user(self, role):
        user_details = {"id": uuid.uuid4(),
                        "role": role,
                        "access_token": uuid.uuid4(),
                        "logged_in": True}

        result = self.db.create_user(user_details)
        if result["user_created"]:
            return user_details
        else:
            return result

    def get_user(self, user_id, access_token):
        fetched_user = self.db.get_user(user_id)
        if fetched_user["user_fetched"]:
            if fetched_user["access_token"] == access_token:
                return fetched_user
            else:
                return {"user_fetched": False,
                        "error": ERROR_UNAUTHORISED_REQUEST}
        else:
            return fetched_user

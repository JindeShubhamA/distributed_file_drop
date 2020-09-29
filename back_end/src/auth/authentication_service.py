import uuid
import user_db
# import user_db

ERROR_UNAUTHORISED_REQUEST = "User not authorised to fetch this resource"


class Authenticator:
    def __init__(self, auth_db: user_db.UserDB):
        self.db = auth_db

    def create_user(self, role):
        user_details = {"id": uuid.uuid4(),
                        "role": role,
                        "access_token": uuid.uuid4(),
                        "logged_in": True}

        result = self.db.create_user(user_details)
        if result["user_created"]:
            user_details["user_created"] = True
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

    def login(self, user_id):
        access_token = uuid.uuid4()
        result = self.db.login(user_id, access_token)
        if result["user_logged_in"]:
            result["access_token"] = access_token
            return result
        else:
            return result

    def logout(self, user_id):
        return self.db.logout(user_id)
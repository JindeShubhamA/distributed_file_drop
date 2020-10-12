from src.file_uploader import redis_driver
# import redis_driver

STATUS_FILE_CACHED = "File stored in cache"
STATUS_FILE_UPLOADED = "File uplaoded successfully"


class IndexCache:
    def __init__(self, redis_config):
        self.redis = redis_driver.RedisDriver(redis_config)

    def create(self, file_name):
        index_key = self.__get_key(file_name)
        result = self.redis.set(index_key, STATUS_FILE_CACHED)
        return result

    def update(self, file_name, updated_status):
        index_key = self.__get_key(file_name)

        result = self.__check_if_index_key_exists(index_key)
        if not result["success"]:
            return result

        result = self.redis.set(index_key, updated_status)
        return result

    def __check_if_index_key_exists(self, file_name):
        return self.redis.get(file_name)

    def __get_key(self, file_name):
        return "file_index:" + file_name
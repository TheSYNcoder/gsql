import json
import os
from gsql.logging import logger


class CacheDict:

    Dict = {}

    def keys_exists(keystore, *keys):
        """
        Check if *keys (nested) exists in `keystore` (dict).
        """
        _keystore = keystore
        for key in keys:
            try:
                _keystore = _keystore[key]
            except KeyError:
                return False
        return True

    def count_lines_in_json(filename="log_data.json"):
        """
        Count number of lines in a json file.
        """
        with open(filename, "r") as file:
            file_data = json.load(file)
            return len(file_data)

    def check_json_file_exists(filename="log_data.json") -> bool:
        if os.path.exists(filename):
            return True
        else:
            return False

    def create_json_file(filename="log_data.json"):
        with open(filename, "w") as file:
            logger.info("File created successfully")
            json.dump({}, file)
            file.close()

    def remove_key_from_json(keypair, filename="log_data.json"):
        """
        Remove key from json if exits
        """
        if CacheDict.check_json_file_exists() is True:
            with open(filename, "r") as file:
                file_data = json.load(file)
                if CacheDict.keys_exists(file_data, keypair) is True:
                    del file_data[keypair]
                    logger.info("key removed successfully from file")
            with open(filename, "w") as modified_file:
                json.dump(file_data, modified_file, indent=2)
                logger.debug("file modified successfully")
        else:
            logger.info("file does not exists")

    def read_from_json(keypair, querypair, filename="log_data.json"):
        with open(filename, "r") as file:
            file_data = json.load(file)
            if CacheDict.keys_exists(file_data, keypair, querypair):
                logger.info("Data present in log file")
                return file_data[keypair][querypair]

    def append_to_json(data, filename="log_data.json", *keys):
        with open(filename, "r+") as file:
            file_data = json.load(file)
            if CacheDict.keys_exists(file_data, keys[0]) is False:
                file_data[keys[0]] = {}
            file_data[keys[0]][keys[1]] = data
            file.seek(0)
            json.dump(file_data, file, indent=2)
            logger.info("Data appended successfully...............")

    def write_to_json(data, *keys):
        filename = "log_data.json"
        CacheDict.append_to_json(data, filename, *keys)

from functools import lru_cache
from key_pair import Keypair
from gsql.cache.cache_handler import (
    CacheDict,
    check_json_file_exists,
    count_lines_in_json,
    create_json_file,
    keys_exists,
    read_from_json,
    remove_key_from_json,
    write_to_json,
)
from gsql.cache.constant import MAXIMUM_SIZE_OF_JSON_FILE


"""
    Cachekey contains the type of query,
    the query itself, database id and the sheet id.
"""


class Cachekey:
    def __init__(self, query_type, query, db_id, sheet_id) -> None:
        self.query_type = query_type
        self.query = query
        self.db_id = db_id
        self.sheet_id = sheet_id

    @lru_cache(maxsize=10000)
    def validate(self):
        """
        Check if the query is executed before
        """
        keypair = Keypair(self.db_id, self.sheet_id).generate_hash()
        if self.query_type == "D" or self.query_type == "U":
            if keys_exists(CacheDict, keypair) is True:
                del CacheDict[keypair]
            else:
                print("Query not in cache...")
            remove_key_from_json(keypair)
            self.clear_cache()
            return None
        querykey = Keypair(self.query, keypair).generate_hash()
        if keys_exists(CacheDict, keypair, querykey):
            print("Key found in the cache.....")
            return CacheDict[keypair][querykey]
        else:
            file_exists = check_json_file_exists()
            if not file_exists:
                create_json_file()
            read_data = read_from_json(keypair, querykey)
            if keys_exists(CacheDict, keypair) is False:
                CacheDict[keypair] = {}
            if read_data is None:
                # call to database
                print("Key not found in the log file.....")
                value = "database call value"
                CacheDict[keypair][querykey] = value
                write_to_json(value, keypair, querykey)
            else:
                print("Key found in log file, please wait.....")
                CacheDict[keypair][querykey] = read_data
                return read_data

    def clear_cache(self):
        """
        clear the lru cache once completed
        """
        self.validate.cache_clear()

    def print_current_and_maxm_contents(filename):
        if check_json_file_exists():
            print("Number of lines in json", count_lines_in_json())
            print("Maximum lines in json ", MAXIMUM_SIZE_OF_JSON_FILE)

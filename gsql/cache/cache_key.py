from key_pair import Keypair
from gsql.cache.cache_handler import CacheDict
from gsql.cache.constant import MAXIMUM_SIZE_OF_JSON_FILE
from gsql.logging import logger

CACHE = CacheDict.Dict


class Cachekey:
    """
    Cachekey contains the type of query,
    the query itself, database id and the sheet id.
    """

    def __init__(self, query_type, query, db_id, sheet_id) -> None:
        self.query_type = query_type
        self.query = query
        self.db_id = db_id
        self.sheet_id = sheet_id

    def validate(self):
        """
        Check if the query is executed before based on the type of query
        """
        keypair = Keypair(self.db_id, self.sheet_id).generate_hash()
        if self.query_type == "D" or self.query_type == "U":
            if CacheDict.keys_exists(CACHE, keypair) is True:
                logger.debug("Query found in cache dict..")
                del CACHE[keypair]
                logger.info("Deleted suceesfully from cache dict..")
            else:
                logger.debug("Query not found in cache dict...")
            CacheDict.remove_key_from_json(keypair)
            return None

        querykey = Keypair(self.query, keypair).generate_hash()
        if CacheDict.keys_exists(CACHE, keypair, querykey):
            logger.debug("Key found in the cache dict..")
            return CACHE[keypair][querykey]
        else:
            file_exists = CacheDict.check_json_file_exists()
            if not file_exists:
                CacheDict.create_json_file()

            read_data = CacheDict.read_from_json(keypair, querykey)
            if CacheDict.keys_exists(CACHE, keypair) is False:
                CACHE[keypair] = {}

            if read_data is None:
                # call to database
                logger.debug("Key not found in the log file.....")
                value = "database call value"
                CACHE[keypair][querykey] = value
                CacheDict.write_to_json(value, keypair, querykey)

            else:
                logger.debug("Key found in log file, please wait.....")
                CACHE[keypair][querykey] = read_data
                return read_data

    def current_and_maxm_contents(filename):
        if CacheDict.check_json_file_exists():
            print("Number of lines in json", CacheDict.count_lines_in_json())
            print("Maximum lines in json ", MAXIMUM_SIZE_OF_JSON_FILE)

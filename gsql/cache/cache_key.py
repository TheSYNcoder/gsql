from functools import lru_cache
from gsql.logging import logger
from key_pair import Keypair
from gsql.cache.cache_handler import CacheDict, check_json_file_exists, create_json_file, keys_exists, read_from_json, remove_key_from_json, write_to_json



''' 
    Cachekey contains the type of query,
    the query itself, database id and the sheet id.
'''
class Cachekey:
    
    def __init__(self, query_type, query, db_id, sheet_id) -> None:
        self.query_type = query_type
        self.query = query
        self.db_id = db_id
        self.sheet_id = sheet_id
    
    
    @lru_cache(maxsize=10000)
    def validate(self):
        ''' 
            Check if the query is executed before 
        '''
        keypair = Keypair(self.db_id, self.sheet_id).generate_hash()
        if self.query_type == 'D' or self.query_type == 'U':
            if keys_exists(CacheDict, keypair) == True:
                del CacheDict[keypair]
                # self.clear_cache()
            else:
                logger.info('Query not in cache...')
            remove_key_from_json(keypair)
            return
        querykey = Keypair(self.query, keypair).generate_hash()
        if keys_exists(CacheDict, keypair, querykey):
            logger.debug("Key found in the cache.....")
            return CacheDict[keypair][querykey]
        else:
            file_exists = check_json_file_exists()
            if not file_exists:
                create_json_file()
            read_data = read_from_json(keypair, querykey)
            if keys_exists(CacheDict, keypair) == False:
                CacheDict[keypair] = {}
            if read_data == None:
                # call to database
                logger.debug("Key not found in the log file.....")
                value = "database call value"
                CacheDict[keypair][querykey] = value
                write_to_json(value, keypair, querykey)
            else:
                logger.debug("Key found in log file, please wait.....")
                CacheDict[keypair][querykey] = read_data
                return read_data
                

    
    def clear_cache(self):
        '''
            clear the lru cache once completed 
        '''
        self.validate.cache_clear()

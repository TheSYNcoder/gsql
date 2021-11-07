import json
from gsql.logging import logger
import os
from json.decoder import JSONDecodeError

CacheDict = { }

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least three arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True



def check_json_file_exists(filename = 'log_data.json') -> bool:
    if os.path.exists(filename):
        return True
    else:
        return False



def create_json_file(filename = 'log_data.json'):
    with open(filename, 'w') as file:
        logger.info('File created successfully')
        json.dump({}, file)
        file.close()



def remove_key_from_json(keypair, filename = 'log_data.json'):
    with open(filename, 'r') as file:
        try:
            file_data = json.load(file)
            if keys_exists(file_data, keypair) == True:
                del file_data[keypair]
                logger.info("key removed successfully from file ")
                print(file_data)
        except JSONDecodeError as error:
                print(error)
    with open(filename, 'w') as modified_file:
        try:
            json.dump(file_data, modified_file, indent=2)
            logger.info("file modified successfully")
        except JSONDecodeError as error:
            print(error)
    
        



def read_from_json(keypair, querypair,  filename = 'log_data.json'):
    if check_json_file_exists(filename) == True:
        with open(filename, 'r') as file:
            try:
                file_data = json.load(file)
                if keys_exists(file_data, keypair, querypair):
                    return file_data[keypair][querypair]
            except JSONDecodeError as error:
                print(error)





def append_to_json(data, filename = 'log_data.json', *keys):
    with open(filename, 'r+') as file:
        try:
            file_data = json.load(file)
            if keys_exists(file_data, keys[0]) == False:
                file_data[keys[0]] = {}
            file_data[keys[0]][keys[1]] = data
            file.seek(0)
            json.dump(file_data, file, indent=2)
            logger.info('Data appended successfully...............')
        except JSONDecodeError as error:
            print(error)
            


def write_to_json(data, *keys):
    filename = 'log_data.json'
    if len(keys) == 0:
        raise AttributeError('write_to_json() expects at least one argument, none given.')
    else:
        append_to_json(data, filename, *keys)
    


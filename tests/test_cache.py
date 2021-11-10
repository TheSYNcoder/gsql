import os
import pytest

from gsql.cache.cache_handler import CacheDict
from gsql.cache.cache_key import Cachekey


def remove_json_file(filename="log_data.json"):
    if CacheDict.check_json_file_exists(filename) is True:
        os.remove(filename)


def clear_dict():
    CacheDict.Dict.clear()


@pytest.fixture(scope="function")
def make_dummy_cachekey():
    ckq1 = Cachekey("R", "SELECT * FROM cache", "QWERTYUasddgs", "1234567")
    ckq2 = Cachekey("R", "fdshjkbsf afkjjbaefkhjeb", "QWERTYUasddgs", "1234567")
    ckq3 = Cachekey("R", "REdGH * FROM cache", "dghjhkjxxfhgvhjkj", "65451321")
    ckq4 = Cachekey("R", "gyjjjjjjjh khbbjblbh", "dghjhkjxxfhgvhjkj", "65451321")
    ckq5 = Cachekey("D", "dhjvdskhskvfhekvf", "dghjhkjxxfhgvhjkj", "65451321")
    ckq6 = Cachekey("D", "SELECT * FROM cache", "QWERTYUasddgs", "1234567")
    return locals()


def test_validate_delete_key_when_file_not_exists(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq5"]
    instance.validate()
    assert "Query not found in cache dict..." == caplog.records[0].msg
    assert "file does not exists" == caplog.records[1].msg


def test_validate_with_write_to_json(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured0 = caplog.records[0].msg
    captured1 = caplog.records[1].msg
    captured2 = caplog.records[2].msg
    assert "File created successfully" in captured0
    assert "Key not found in the log file....." in captured1
    assert "Data appended successfully..............." in captured2
    instance = make_dummy_cachekey["ckq3"]
    instance.validate()
    assert "File created successfully" in captured0
    assert "Key not found in the log file....." in captured1
    assert "Data appended successfully..............." in captured2


def test_validate_with_write_to_json_same_key(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured = caplog.records[0].msg
    assert "Key found in the cache dict.." in captured


def test_validate_delete_from_existing_dict(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq6"]
    instance.validate()
    assert "Query found in cache dict.." in caplog.records[0].msg
    assert "Deleted suceesfully from cache dict.." in caplog.records[1].msg
    assert "key removed successfully from file" in caplog.records[2].msg
    assert "file modified successfully" in caplog.records[3].msg


def test_validate_with_write_to_json_temp(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured0 = caplog.records[0].msg
    captured1 = caplog.records[1].msg
    assert "Key not found in the log file....." in captured0
    assert "Data appended successfully..............." in captured1


def test_validate_with_read_from_files(make_dummy_cachekey, caplog):
    clear_dict()
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured0 = caplog.records[0].msg
    captured1 = caplog.records[1].msg
    assert "Data present in log file" in captured0
    assert "Key found in log file, please wait....." in captured1


def test_validate_with_delete_key_in_file_exits(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq5"]
    instance.validate()
    assert "Query not found in cache dict..." in caplog.records[0].msg
    assert "key removed successfully from file" in caplog.records[1].msg
    assert "file modified successfully" in caplog.records[2].msg


def test_count_lines_in_file(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq4"]
    instance.current_and_maxm_contents()
    captured = capsys.readouterr().out
    assert "Number of lines in json 1\nMaximum lines in json  1000\n" == captured


def test_validate_with_delete_key_not_exists_in_file(make_dummy_cachekey, caplog):
    instance = make_dummy_cachekey["ckq5"]
    instance.validate()
    captured0 = caplog.records[0].msg
    captured1 = caplog.records[1].msg
    assert "Query not found in cache dict..." in captured0
    assert "file modified successfully" in captured1
    remove_json_file()

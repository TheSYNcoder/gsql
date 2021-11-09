import os
import pytest

from gsql.cache.cache_handler import CacheDict, check_json_file_exists
from gsql.cache.cache_key import Cachekey


def remove_json_file(filename="log_data.json"):
    if check_json_file_exists(filename) is True:
        os.remove(filename)


def clear_dict():
    CacheDict.clear()


@pytest.fixture(scope="function")
def make_dummy_cachekey():
    ckq1 = Cachekey("R", "SELECT * FROM cache", "QWERTYUasddgs", "1234567")
    ckq2 = Cachekey("R", "fdshjkbsf afkjjbaefkhjeb", "QWERTYUasddgs", "1234567")
    ckq3 = Cachekey("R", "REdGH * FROM cache", "dghjhkjxxfhgvhjkj", "65451321")
    ckq4 = Cachekey("R", "gyjjjjjjjh khbbjblbh", "dghjhkjxxfhgvhjkj", "65451321")
    ckq5 = c2 = Cachekey("D", "dhjvdskhskvfhekvf", "dghjhkjxxfhgvhjkj", "65451321")
    ckq6 = Cachekey("R", "SELECT * FROM cache", "QWERTYUasddgs", "1234567")
    return locals()


def test_validate_delete_key_when_file_not_exists(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq5"]
    instance.validate()
    captured = capsys.readouterr().out
    assert "file does not exists" in captured


def test_validate_with_write_to_json(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured = capsys.readouterr().out
    assert "Key not found in the log file....." in captured
    instance = make_dummy_cachekey["ckq3"]
    instance.validate()
    captured = capsys.readouterr().out
    assert "Key not found in the log file....." in captured


def test_validate_with_write_to_json_same_key(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured = capsys.readouterr().out
    assert "Key found in the cache....." in captured


def test_validate_with_read_from_files(make_dummy_cachekey, capsys):
    clear_dict()
    instance = make_dummy_cachekey["ckq1"]
    instance.validate()
    captured = capsys.readouterr().out
    assert (
        "Data present in json file\nKey found in log file, please wait.....\n"
        in captured
    )


def test_validate_with_delete_key_in_file_exits(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq5"]
    instance.validate()
    captured = capsys.readouterr().out
    assert "key removed successfully from file" in captured


def test_count_lines_in_file(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq4"]
    instance.print_current_and_maxm_contents()
    captured = capsys.readouterr().out
    assert "Number of lines in json 1\nMaximum lines in json  10000\n" == captured


def test_validate_with_delete_key_not_exists_in_file(make_dummy_cachekey, capsys):
    instance = make_dummy_cachekey["ckq5"]
    instance.validate()
    captured = capsys.readouterr().out
    assert "Query not in cache...\nfile modified successfully" in captured
    remove_json_file()

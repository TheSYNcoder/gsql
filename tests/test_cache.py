import pytest
import json
import pathlib
from gsql.cache.cache_key import Cachekey
from gsql.cache.key_pair import Keypair


@pytest.fixture(scope="session")
def make_dummy_db_sheet_hash():
    dbs1 = Keypair("  qwerty", "12345  ")
    dbs2 = Keypair("  gvhjjkn", "1654454  ")
    return locals()


@pytest.fixture(scope="session")
def make_dummy_db_sheet_query_hash(make_dummy_db_sheet_hash):
    dbsq1 = Keypair(
        make_dummy_db_sheet_hash["dbs1"].generate_hash(), "select * from table"
    )
    dbsq2 = Keypair(make_dummy_db_sheet_hash["dbs2"].generate_hash(), "update from db")
    return locals()


@pytest.fixture(scope="session")
def make_dummy_cachekey():
    ckq1 = Cachekey("R", "SELECT * FROM cache", "QWERTYUasddgs", "1234567")
    ckq2 = Cachekey("R", "fdshjkbsf afkjjbaefkhjeb", "QWERTYUasddgs", "1234567")
    ckq3 = Cachekey("R", "REdGH * FROM cache", "dghjhkjxxfhgvhjkj", "65451321")
    ckq4 = Cachekey("R", "gyjjjjjjjh khbbjblbh", "dghjhkjxxfhgvhjkj", "65451321")
    ckq5 = c2 = Cachekey("D", "dhjvdskhskvfhekvf", "dghjhkjxxfhgvhjkj", "65451321")
    return locals()


@pytest.fixture(autouse=True)
def read_config(request):
    file = pathlib.Path(request.node.fspath)
    print("current test file:", file)
    log_data_file = file.with_name("log_data.json")
    print("current log_data_file file:", log_data_file)
    with log_data_file.open() as fp:
        contents = json.load(fp)
    print("log_data_file contents:", contents)


def test_generate_db_sheet_hash(make_dummy_db_sheet_hash, capsys):
    captured = capsys.readouterr()
    make_dummy_db_sheet_hash["dbs1"].generate_hash() in captured.out
    make_dummy_db_sheet_hash["dbs2"].generate_hash() in captured.out


def test_generate_db_sheet_query_hash(make_dummy_db_sheet_query_hash, capsys):
    captured = capsys.readouterr()
    make_dummy_db_sheet_query_hash["dbsq1"].generate_hash() in captured.out
    make_dummy_db_sheet_query_hash["dbsq2"].generate_hash() in captured.out

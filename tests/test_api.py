from gsql.backend import api_handler
from googleapiclient import errors


def test_init_success(monkeypatch, caplog):
    def mock_build_success(*args, **kwargs):
        return "mock_build_obj"

    monkeypatch.setattr(api_handler, "build", mock_build_success)
    instance = api_handler.ApiHandler("creds")
    assert instance.creds == "creds"
    assert instance.gdriveService == "mock_build_obj"
    assert instance.sheetService == "mock_build_obj"


def test_init_failure(monkeypatch, mocker, caplog):
    def mock_build_failure(*args, **kwargs):
        raise errors.Error("invalid cred")

    monkeypatch.setattr(api_handler, "build", mock_build_failure)
    instance = api_handler.ApiHandler("creds")
    assert instance.creds == "creds"
    assert caplog.records[0].msg == "driver creation failed with error: invalid cred"

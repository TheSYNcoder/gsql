from gsql.backend.auth import os, Auth, Credentials, InstalledAppFlow
from googleapiclient import errors


def test_logout_success(monkeypatch, mocker):
    mocker.patch.object(os, "remove")
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")
    instance = Auth()
    instance.logout()
    os.remove.assert_called_with("temp/token.json")


def test_logout_failure(monkeypatch, mocker, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    def mock_os_remove(*args, **kwargs):
        raise Exception("mocking os.remove failure")

    monkeypatch.setattr(os, "remove", mock_os_remove)
    instance = Auth()
    instance.logout()
    assert caplog.records[0].msg == "mocking os.remove failure"


def test_login_valid_creds(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    class Cred_mock:
        def __init__(self, valid) -> None:
            self.valid = valid

    def mock_cred_making(*args, **kwargs):
        return Cred_mock(True)

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)
    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "Authentication successfull"


def test_login_expired_cred(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    class Cred_mock:
        def __init__(self) -> None:
            self.valid = False
            self.expired = True
            self.refresh_token = True

        def refresh(*args, **kwargs):
            print("mock")

    def mock_cred_making(*args, **kwargs):
        return Cred_mock()

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)

    def mock_Auth_save_token(*args, **kwargs):
        print("done")

    monkeypatch.setattr(Auth, "save_token", mock_Auth_save_token)
    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "refresh token called!!!"
    assert caplog.records[2].msg == "Authentication successfull"


def test_login_expired_error_refresh(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    class Cred_mock:
        def __init__(self) -> None:
            self.valid = False
            self.expired = True
            self.refresh_token = True

        def refresh(*args, **kwargs):
            raise errors.Error("mock")

    def mock_cred_making(*args, **kwargs):
        return Cred_mock()

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)

    def mock_Auth_save_token(*args, **kwargs):
        print("mock")

    monkeypatch.setattr(Auth, "save_token", mock_Auth_save_token)
    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "refresh token called!!!"
    assert caplog.records[2].msg == "Authentication failed: mock"


def test_login_again_error_file(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    def mock_cred_making(*args, **kwargs):
        return False

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)

    def mock_Auth_save_token(*args, **kwargs):
        print("mock")

    monkeypatch.setattr(Auth, "save_token", mock_Auth_save_token)

    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "relogin called"
    assert (
        caplog.records[2].msg
        == "Credentials.json file not found in specified directory"
    )


def test_login_again_success(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    def mock_cred_making(*args, **kwargs):
        return False

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)

    def mock_Auth_save_token(*args, **kwargs):
        print("mock")

    monkeypatch.setattr(Auth, "save_token", mock_Auth_save_token)

    class Mock_flow:
        def run_local_server(*args, **kwargs):
            return True

    def mock_flow(*args, **kwargs):
        return Mock_flow()

    monkeypatch.setattr(InstalledAppFlow, "from_client_secrets_file", mock_flow)
    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "relogin called"
    assert caplog.records[2].msg == "Authentication successfull"


def test_login_again_error_flow_error(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    def mock_cred_making(*args, **kwargs):
        return False

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)

    def mock_Auth_save_token(*args, **kwargs):
        print("mock")

    monkeypatch.setattr(Auth, "save_token", mock_Auth_save_token)

    class Mock_flow:
        def run_local_server(*args, **kwargs):
            raise errors.Error("error")

    def mock_flow(*args, **kwargs):
        return Mock_flow()

    monkeypatch.setattr(InstalledAppFlow, "from_client_secrets_file", mock_flow)
    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "relogin called"
    assert caplog.records[2].msg == "Error returned -> error"


def test_login_again_error_flow_exception(mocker, monkeypatch, caplog):
    mocker.patch.object(os.path, "join")
    os.path.join.return_value = "temp/"
    mocker.patch.object(os.path, "exists")
    os.path.exists.return_value = True
    mocker.patch.object(os, "makedirs")

    def mock_cred_making(*args, **kwargs):
        return False

    monkeypatch.setattr(Credentials, "from_authorized_user_file", mock_cred_making)

    def mock_Auth_save_token(*args, **kwargs):
        print("mock")

    monkeypatch.setattr(Auth, "save_token", mock_Auth_save_token)

    class Mock_flow:
        def run_local_server(*args, **kwargs):
            raise Exception("exception")

    def mock_flow(*args, **kwargs):
        return Mock_flow()

    monkeypatch.setattr(InstalledAppFlow, "from_client_secrets_file", mock_flow)
    instance = Auth()
    instance.auth()
    assert caplog.records[0].msg == "importing cred from token.json"
    assert caplog.records[1].msg == "relogin called"
    assert caplog.records[2].msg == "Error returned -> exception"

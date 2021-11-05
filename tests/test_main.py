from gsql.frontend.arg_parser import get_arguments
from gsql.frontend.constants import Commands
from gsql.exceptions.frontend.arg_exception import ArgumentException
import sys
import pytest
from gsql.main import app
import io
from gsql.frontend.shell.driver import Auth


def test_main_app(monkeypatch, caplog):
    monkeypatch.setattr("sys.stdin", io.StringIO("exit"))
    sys.argv = ["gsql"]

    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("SHELL")


def test_main_app_with_authenticate_success(caplog, capsys):

    Auth.auth = lambda x: False
    sys.argv = ["gsql", "login"]
    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("LOGIN")
    assert caplog.records[2].msg == "Authentication successfull"


def test_main_app_with_authenticate_fail(caplog, capsys):

    Auth.auth = lambda x: True
    sys.argv = ["gsql", "login"]
    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("LOGIN")
    assert caplog.records[2].msg == "Authentication failed: True"


def test_main_app_with_logout_success(caplog, capsys):
    Auth.logout = lambda x: False
    sys.argv = ["gsql", "logout"]
    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("LOGOUT")
    assert caplog.records[2].msg == "Logout successfull"


def test_main_app_with_logout_failed(caplog, capsys):
    Auth.logout = lambda x: True
    sys.argv = ["gsql", "logout"]
    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("LOGOUT")
    assert caplog.records[2].msg == "Logout failed: True"


def test_main_app_with_show(caplog, capsys):
    sys.argv = ["gsql", "show"]

    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("SHOW")
    captured = capsys.readouterr()
    assert "show" in captured.out


def test_main_app_with_help(caplog, capsys):
    sys.argv = ["gsql", "help"]

    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("HELP")
    captured = capsys.readouterr()
    assert "help" in captured.out


def test_main_app_with_error(caplog, capsys):
    sys.argv = ["gsql", "error"]

    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("ERROR")
    captured = capsys.readouterr()
    assert "error" in captured.out


def test_arguments_gsql_shell(caplog):
    sys.argv = ["gsql"]
    action = get_arguments()
    assert action == Commands.SHELL_COMMAND


def test_arguments_gsql_login(caplog):

    sys.argv = ["gsql", "login"]
    action = get_arguments()
    assert action == Commands.LOGIN_COMMAND


def test_arguments_gsql_logout(caplog):

    sys.argv = ["gsql", "logout"]
    action = get_arguments()
    assert action == Commands.LOGOUT_COMMAND


def test_arguments_gsql_show(caplog):

    sys.argv = ["gsql", "show"]
    action = get_arguments()
    assert action == Commands.SHOW_COMMAND


def test_arguments_error_input(caplog):

    sys.argv = ["gsql", "random_input"]
    action = get_arguments()
    assert action == Commands.ERROR


def test_arguments_help(caplog):

    sys.argv = ["gsql", "help"]
    action = get_arguments()
    assert action == Commands.HELP_COMMAND


def test_arguments_exception_raised_when_moreThanTwoArguments():

    sys.argv = ["gsql", "one", "two", "three"]
    with pytest.raises(ArgumentException):
        _ = get_arguments()

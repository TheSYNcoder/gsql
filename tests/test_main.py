from gsql.frontend.arg_parser import get_arguments
from gsql.frontend.constants import Commands
from gsql.exceptions.frontend.arg_exception import ArgumentException
import sys
import pytest
from gsql.main import app
import io


def test_main_app(monkeypatch, caplog):
    monkeypatch.setattr("sys.stdin", io.StringIO("exit"))
    sys.argv = ["gsql"]

    app()
    assert caplog.records[0].msg == "GSQL APP INIT"
    assert caplog.records[1].msg == "GSQL called with action :{}".format("SHELL")


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


def test_arguments_gsql_clear(caplog):

    sys.argv = ["gsql", "clear"]
    action = get_arguments()
    assert action == Commands.CLEAR_COMMAND


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

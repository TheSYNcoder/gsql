from gsql.frontend.shell.shell import GSQLShell
from rich.table import Table
import os
import io
import pytest
from rich.console import Console


def test_shell_precmd_clear(monkeypatch, mocker):

    monkeypatch.setattr("sys.stdin", io.StringIO("CLEAR\nEXIT"))
    mocker.patch.object(os, "system")
    instance = GSQLShell()
    instance.cmdloop()
    os.system.assert_called_with("clear")


def test_shell_precmd_cls(monkeypatch, mocker):

    monkeypatch.setattr("sys.stdin", io.StringIO("CLEAR\nEXIT"))
    mocker.patch.object(os, "system")
    mocker.patch.object(os, "name")
    os.name.return_value = "windows"
    instance = GSQLShell()
    instance.cmdloop()
    os.system.assert_called_with("cls")


def test_shell_precmd_connect_correctly(monkeypatch):

    monkeypatch.setattr(
        "sys.stdin", io.StringIO("CONNECT 1WooAUEpz7ECEK2M7YIS3WzNK2c\nEXIT")
    )
    instance = GSQLShell()
    instance.cmdloop()
    sheet_name = "Fun Sheet"
    assert instance.prompt == f'GSQL ({sheet_name.replace(" ", "")[:10]}) > '


def test_shell_precmd_connect_error(monkeypatch, capsys):

    monkeypatch.setattr("sys.stdin", io.StringIO("CONNECT random\nEXIT"))
    instance = GSQLShell()
    instance.cmdloop()
    captured = capsys.readouterr()

    assert "Database with id: random not found" in captured.out


def test_shell_precmd_connect_wrong_args(monkeypatch, capsys):

    monkeypatch.setattr("sys.stdin", io.StringIO("CONNECT\nEXIT"))
    instance = GSQLShell()
    instance.cmdloop()
    captured = capsys.readouterr()
    line = "connect "
    assert f"error: gsql: {line} not recognized" in captured.out


def test_shell_precmd_disconnect(monkeypatch, capsys):

    monkeypatch.setattr("sys.stdin", io.StringIO("DISCONNECT\nEXIT"))
    instance = GSQLShell()
    instance.cmdloop()
    captured = capsys.readouterr()
    assert instance.prompt == "GSQL > "
    assert "Disconnected successfully" in captured.out


@pytest.fixture
def table_data():
    sheets = [
        {"name": "Fun Sheet", "id": "1WooAUEpz7ECEK2M7YIS3WzNK2c"},
        {"name": "Another Fun Sheet", "id": "qjdq286382bhd27872gr44"},
    ]
    table = Table(title="Your databases")
    table.add_column("Serial", justify="right", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("ID", justify="right")
    # limiting display upto first 20 sheets
    to_be_shown = sheets[:20]
    for i, item in enumerate(to_be_shown):
        table.add_row(str(i + 1), item["name"], item["id"])
    return table


def test_get_tables_correctly(monkeypatch, table_data, capsys):

    monkeypatch.setattr("sys.stdin", io.StringIO("SHOW DATABASES\nEXIT"))
    instance = GSQLShell()
    instance.cmdloop()
    instance.sheets = [
        {"name": "Fun Sheet", "id": "1WooAUEpz7ECEK2M7YIS3WzNK2c"},
        {"name": "Another Fun Sheet", "id": "qjdq286382bhd27872gr44"},
    ]
    captured = capsys.readouterr()
    console = Console(file=io.StringIO(), width=120)
    console.print(table_data)
    output = console.file.getvalue()
    assert output in captured.out


def test_get_tables_incorrectly(monkeypatch, table_data, capsys):

    monkeypatch.setattr("sys.stdin", io.StringIO("SHOW\nEXIT"))
    instance = GSQLShell()
    instance.cmdloop()

    captured = capsys.readouterr()
    line = "show "
    assert f"error: gsql: {line} not recognized" in captured.out

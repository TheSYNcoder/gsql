

from gsql.frontend.shell.shell import GSQLShell
import os
import io
import sys
import pytest





def test_shell_precmd_clear(monkeypatch, mocker):

    monkeypatch.setattr("sys.stdin", io.StringIO("CLEAR\nEXIT"))
    mocker.patch.object(os, 'system')
    instance = GSQLShell()
    instance.cmdloop()             
    os.system.assert_called_with('clear')

def test_shell_precmd_cls(monkeypatch, mocker):

    monkeypatch.setattr("sys.stdin", io.StringIO("CLEAR\nEXIT"))
    mocker.patch.object(os, 'system')
    mocker.patch.object(os, 'name')
    os.name.return_value = 'windows'
    instance = GSQLShell()
    instance.cmdloop()             
    os.system.assert_called_with('cls')


def test_shell_precmd_connect_correctly(monkeypatch, mocker):

    monkeypatch.setattr("sys.stdin", io.StringIO("CONNECT 1WooAUEpz7ECEK2M7YIS3WzNK2c\nEXIT"))
    instance = GSQLShell()
    instance.cmdloop()  
    sheet_name = 'Fun Sheet'
    assert instance.prompt == f'GSQL ({sheet_name.replace(" ", "")[:10]}) > '
    
    



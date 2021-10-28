import os
import cmd

try:
    import readline
except ImportError:
    readline = None

from gsql.console import console
from rich.table import Table
import time


gsql_text = """
    ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌
▐░▌ ▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌
▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌
▐░▌ ▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌
▐░▌       ▐░▌          ▐░▌▐░░░░░░░░░░░▌▐░▌
▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌ ▀▀▀▀▀▀█░█▀▀ ▐░█▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌        ▐░▌  ▐░░░░░░░░░░░▌
▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀          ▀    ▀▀▀▀▀▀▀▀▀▀▀"""


class GSQLShell(cmd.Cmd):

    intro = gsql_text
    prompt = "GSQL > "

    def __init__(self) -> None:
        super(GSQLShell, self).__init__()
        self.history_file = os.path.join(
            os.path.expanduser("~"), ".gsql", "gsql_history.txt"
        )
        self.histfile_size = 1000
        # dummy data
        self.sheets = [
            {"name": "Fun Sheet", "id": "1WooAUEpz7ECEK2M7YIS3WzNK2c"},
            {"name": "Another Fun Sheet", "id": "qjdq286382bhd27872gr44"},
        ]

    def preloop(self):
        if readline and os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)

    def default(self, line):
        """
        Prints out an error message to the console
        """
        console.print(f"[red]error: gsql: {line} not recognized[/]")

    def do_show(self, args):
        """
        Show
        ------------
        Command to show the current databases ( google sheets ) available
        in your account.
        Usage : show databases
         - Prints out name and id of the spreadsheets
        """

        arg_tokens = args.split()
        if len(arg_tokens) != 1 or arg_tokens[0].lower() != "databases":
            self.default("show " + args)
            return

        # TODO get the details from API

        with console.status("Getting your data ....", spinner="bouncingBall"):
            # call API synchronous call
            time.sleep(3)

        table = Table(title="Your databases")
        table.add_column("Serial", justify="right", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("ID", justify="right")
        # limiting display upto first 20 sheets
        to_be_shown = self.sheets[:20]
        for i, item in enumerate(to_be_shown):
            table.add_row(str(i + 1), item["name"], item["id"])

        console.print(table)

    def do_connect(self, args):
        """
        Connect
        ------------
        Command to connect to the database (google sheet) whose id user provides

        Usage : connect <id>
         - Connects to the database for  further operations on it
        """

        arg_tokens = args.split()
        if len(arg_tokens) != 1:
            self.default("connect " + args)
            return

        sheet_id = arg_tokens[0]

        with console.status("Attempting to connect ....", spinner="bouncingBall"):
            # TODO call API synchronous call
            if sheet_id not in [item["id"] for item in self.sheets]:
                console.print("[red]Database with {id} not found[/]")
            time.sleep(3)
        sheet_name = list(filter(lambda x: x["id"] == sheet_id, self.sheets))[0]["name"]
        self.prompt = "GSQL (" + sheet_name.replace(" ", "")[:10] + ") > "
        console.print(f"[green]Connected to {str(sheet_id)}[/]")

    def do_disconnect(self, args):
        """
        Disconnect
        ------------
        Command to come out of the current session

        Usage : disconnect
            -Disconnect the connection (if any) from the current database
        """

        # TODO make api call and remove from cache
        self.prompt = "GSQL > "
        console.print("[green]Disconnected successfully[/]")

    def do_clear(self, args):
        """
        Clears the GSQL shell
        """
        if os.name == "posix":
            _ = os.system("clear")
        else:
            _ = os.system("cls")

    def precmd(self, line):
        """
        Converts the current line to lowercase
        """
        tokens = str(line).split()
        if tokens[0].lower() == "connect":
            line = "connect " + " ".join(token for token in tokens[1:])
        else:
            line = line.lower()
        return line

    def do_exit(self, args):
        """
        Exit from the GSQL shell
        """
        return True

    def postloop(self):
        if readline:
            readline.set_history_length(self.histfile_size)
            readline.write_history_file(self.history_file)

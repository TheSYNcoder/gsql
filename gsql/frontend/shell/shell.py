from gsql.exceptions.sqlparser_exception import SQLStatmentException
from gsql.backend.auth import Auth
from gsql.backend.api_handler import ApiHandler
from gsql.backend.sqlite_manager import SQLiteManager
from gsql.frontend.sql_parser import SQLParser
import os
import cmd


try:
    import readline
except ImportError:
    readline = None

from gsql.console import console
from rich.table import Table


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

        self.sql_parser = SQLParser()
        self.sqlite_manager = SQLiteManager()
        self.api = ApiHandler(Auth.get_creds())
        self._get_sheets()

    def _get_sheets(self):
        df = self.sqlite_manager._read_from_common()
        self.sheets = df

    def preloop(self):
        if readline and os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)

    def default(self, line):
        """
        Should be a either a valid SQL statement or error
        """
        try:
            self.sql_parser.parse_statement(line)
        except SQLStatmentException as e:
            console.print("[red]{}[/]".format(e.message))

    def _show_error(self, line):
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
              : show tables
         - Prints out the available tables in a databases ( sheets in a spreadsheet )
        """

        arg_tokens = args.split()
        if len(arg_tokens) != 1 or arg_tokens[0].lower() not in ["databases", "tables"]:
            self._show_error("show " + args)
            return

        if arg_tokens[0].lower() == "tables":
            if self.sql_parser.database is None:
                console.print(
                    "[red]error: gsql: Not connected to database, please first connect to a database[/]"
                )
                return

        with console.status("Getting your data ....", spinner="bouncingBall"):
            if arg_tokens[0].lower() == "databases":
                table = Table(title="Your databases")
                table.add_column("Serial", justify="right", no_wrap=True)
                table.add_column("Title", style="green")
                table.add_column("ID", justify="right")
                table.add_column("Nickname", style="green")
                # limiting display upto first 20 sheets
                to_be_shown = self.sheets[:20]
                for i, item in to_be_shown.iterrows():
                    table.add_row(
                        str(i + 1), item["title"], item["id"], item["nickname"]
                    )
            else:
                table = Table(title="Tables")
                table.add_column("Serial", justify="right", no_wrap=True)
                table.add_column("Name", style="green")
                table.add_column("ID", justify="right")
                table.add_column("Row Count")
                table.add_column("Column Count")

                data = self.sqlite_manager.read_metadata(self.sql_parser.database)
                for i, item in data.iterrows():
                    table.add_row(
                        str(i + 1),
                        item["sheet_title"],
                        str(item["sheet_id"]),
                        str(item["row_count"]),
                        str(item["col_count"]),
                    )

        console.print(table)

    def do_connect(self, args):
        """
        Connect
        ------------
        Command to connect to the database (google sheet) whose id user provides

        Usage : connect <title or id or nickname>
         - Connects to the database for  further operations on it
        """

        arg_tokens = args.split()
        if len(arg_tokens) != 1:
            self._show_error("connect " + args)
            return

        sheet_arg = arg_tokens[0]

        with console.status("Attempting to connect ....", spinner="bouncingBall"):
            is_sheet_name = sheet_arg in self.sheets["title"].tolist()
            is_sheet_id = sheet_arg in self.sheets["id"].tolist()
            is_sheet_nickname = sheet_arg in self.sheets["nickname"].tolist()
            if not is_sheet_name and not is_sheet_id and not is_sheet_nickname:
                console.print(f"[red]Database with arg : {sheet_arg} not found[/]")
                return
            if is_sheet_name:
                sheet_name = sheet_arg
                sheet_id = self.sheets.loc[
                    self.sheets["title"] == sheet_arg, "id"
                ].iloc[0]
            elif is_sheet_id:
                sheet_name = self.sheets.loc[
                    self.sheets["id"] == sheet_arg, "title"
                ].iloc[0]
                sheet_id = sheet_arg
            else:
                sheet_name = self.sheets.loc[
                    self.sheets["nickname"] == sheet_arg, "title"
                ].iloc[0]
                sheet_id = self.sheets.loc[
                    self.sheets["nickname"] == sheet_arg, "id"
                ].iloc[0]

            # get the data and store it in sqlite
            metadata = self.api.getSpreadsheetInfo(sheet_id)
            self.sqlite_manager.write_metadata(metadata)
            self.prompt = "GSQL (" + sheet_name.replace(" ", "")[:10] + ") > "
            self.sql_parser.database = sheet_id
        console.print(f"[green]Connected to {str(sheet_id)}[/]")

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd("\n")

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
        del self.sql_parser.database
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

        #  check empty command
        if line == "":
            return line
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

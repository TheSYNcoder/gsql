from gsql.frontend.constants import Commands
from gsql.logging import logger
from gsql.frontend.shell.shell import GSQLShell
from rich import print
from gsql.backend.auth import Auth
from gsql.console import console


class GSQLDriver:
    """
    This is the main driver for the gsql shell
    """

    def __init__(self, action: str) -> None:
        self.action = action
        logger.debug("GSQL called with action :{}".format(self.action))
        self.shell_instance = GSQLShell()

    def authenticate(self):
        auth = Auth()
        err = auth.auth()
        if err:
            logger.error("Authentication failed: {}".format(err))
            console.print("[red]Authentication failed!!!")
        else:
            logger.debug("Authentication successfull")
            console.print("[green]Authentication successfull")

    def logout(self):
        auth = Auth()
        err = auth.logout()
        if err:
            logger.error("Logout failed: {}".format(err))
            console.print("[red]Logout failed!!![/]")
        else:
            logger.debug("Logout successfull")
            console.print("[green]Logout successfull[/]")

    def show(self):
        print("show")

    def show_help(self):
        print("help")

    def start_shell(self):
        self.shell_instance.cmdloop()

    def error_(self):
        print("error")

    def execute(self):

        if self.action == Commands.LOGIN_COMMAND:
            self.authenticate()
        elif self.action == Commands.LOGOUT_COMMAND:
            self.logout()
        elif self.action == Commands.SHOW_COMMAND:
            self.show()
        elif self.action == Commands.HELP_COMMAND:
            self.show_help()
        elif self.action == Commands.ERROR:
            self.error_()
        else:
            self.start_shell()

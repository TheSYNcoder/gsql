from gsql.frontend.constants import Commands
from gsql.logging import logger
from gsql.frontend.shell.shell import GSQLShell
from rich import print


class GSQLDriver:
    """
    This is the main driver for the gsql shell
    """

    def __init__(self, action: str) -> None:
        self.action = action
        logger.debug("GSQL called with action :{}".format(self.action))
        self.shell_instance = GSQLShell()

    def authenticate(self):
        print("Authenticate")

    def clear_shell(self):
        print("shell clear")

    def logout(self):
        print("login")

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
        elif self.action == Commands.CLEAR_COMMAND:
            self.clear_shell()
        elif self.action == Commands.ERROR:
            self.error_()
        else:
            self.start_shell()

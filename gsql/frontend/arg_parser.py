from gsql.frontend.constants import Commands
from gsql.exceptions.frontend.arg_exception import ArgumentException
import sys


def validate_args(args):
    """
    a function to validate the system arguments provided

    validation scheme
    gsql to be called as

    $ gsql <command>?

    There can be at most 2 system arguments
    """
    if len(args) > 2:
        raise ArgumentException(args)
    return args


def get_action_from_argument(args) -> str:
    """
    Determines the action to perform based on arguments

    The action is a string and is one of

    'LOGIN' | 'LOGOUT' | 'HELP' | 'SHOW' | 'CLEAR' | 'SHELL' | 'ERROR'
    """

    if len(args) == 1:
        # case when user has typed `gsql`
        return Commands.SHELL_COMMAND

    command = str(args[1]).lower()

    if command == "login":
        return Commands.LOGIN_COMMAND
    elif command == "logout":
        return Commands.LOGOUT_COMMAND
    elif command == "show":
        return Commands.SHOW_COMMAND
    elif command == "clear":
        return Commands.CLEAR_COMMAND
    elif command == "h" or command == "help":
        return Commands.HELP_COMMAND
    else:
        return Commands.ERROR


def get_arguments():
    """
    Gets all the arguments
    """
    system_arguments = sys.argv
    system_arguments = validate_args(system_arguments)
    return get_action_from_argument(system_arguments)

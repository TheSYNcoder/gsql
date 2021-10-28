from gsql.frontend.shell.driver import GSQLDriver
from gsql.frontend.arg_parser import get_arguments
from gsql.exceptions.frontend.arg_exception import ArgumentException
from gsql.logging import logger
from rich.traceback import install
import sys


def app():
    """
    Main app

    The starting point of gsql
    """
    logger.debug("GSQL APP INIT")
    install()
    # get the arguments passed
    try:
        action = get_arguments()
    except ArgumentException:
        logger.error("gsql: invalid number of arguments")
        sys.exit(0)
    driver = GSQLDriver(action=action)
    driver.execute()

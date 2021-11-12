from gsql.logging import logger
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class Auth:
    def __init__(self) -> None:
        self.creds = None
        self.store_folder = os.path.join(os.path.expanduser("~"), ".gsql")
        os.makedirs(self.store_folder, exist_ok=True)

    def save_token(self):
        with open(os.path.join(self.store_folder, "token.json"), "w") as token:
            token.write(self.creds.to_json())

    @staticmethod
    def get_creds():
        """
        static method to get the credentials
        """
        store_folder = os.path.join(os.path.expanduser("~"), ".gsql")
        return Credentials.from_authorized_user_file(
            os.path.join(store_folder, "token.json"), SCOPES
        )

    def auth(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(self.store_folder, "token.json")):
            self.creds = Credentials.from_authorized_user_file(
                os.path.join(self.store_folder, "token.json"), SCOPES
            )
            logger.debug("importing cred from token.json")
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    logger.debug("refresh token called!!!")
                    self.creds.refresh(Request())
                except errors.Error as err:
                    logger.error("Authentication failed: {}".format(err))
                    return err
            else:
                logger.debug("relogin called")
                err = self.login()
                if err:
                    return err
            # Save the credentials for the next run
            self.save_token()
        logger.debug("Authentication successfull")

    def login(self):
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(self.store_folder, "credentials.json"), SCOPES
            )
            self.creds = flow.run_local_server(port=8080)
        except FileNotFoundError as err:
            logger.error("Credentials.json file not found in specified directory")
            return err
        except errors.Error as err:
            logger.error("Error returned -> {}".format(err))
            return err
        except Exception as err:
            logger.error("Error returned -> {}".format(err))
            return err

    def logout(self):
        store_folder = os.path.join(os.path.expanduser("~"), ".gsql")
        os.makedirs(store_folder, exist_ok=True)
        token_path = os.path.join(store_folder, "token.json")
        if os.path.exists(token_path):
            try:
                os.remove(token_path)
            except Exception as err:
                logger.error(err.__str__())
                return err

from googleapiclient import errors
from googleapiclient.discovery import build
from gsql.logging import logger


class ApiHandler:
    def __init__(self, creds) -> None:
        self.creds = creds
        """
            create service objects for google drive and sheets to access client apis
        """
        try:
            self.gdriveService = build(
                serviceName="sheets", version="v4", credentials=self.creds
            )
            self.sheetService = build(
                serviceName="drive", version="v2", credentials=self.creds
            )
        except errors.Error as err:
            logger.error("driver creation failed with error: {}".format(err))

    #    creation apis

    def createSpreadsheet(self, spreadsheetTitle):
        logger.debug(
            "createSpreadsheet called with sheetTitle: {}".format(spreadsheetTitle)
        )
        body = {"properties": {"title": spreadsheetTitle}}
        try:
            spreadsheet = (
                self.sheetService.spreadsheets()
                .create(body=body, fields="spreadsheetId")
                .execute()
            )
        except errors.Error as err:
            logger.error(
                "creation of spreadheet with title({}) failed with error: {}".format(
                    spreadsheetTitle, err
                )
            )
            return err
        return spreadsheet

    def createTabInsideSpreadsheet(self, spreadsheetId, tabTitle):
        logger.debug(
            "createTabInsideSpreadsheet called with spreadheetId: {} , tabTitle: {}".format(
                spreadsheetId, tabTitle
            )
        )
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": tabTitle,
                        }
                    }
                }
            ]
        }
        try:
            result = (
                self.sheetService.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheetId, body=body)
                .execute()
            )
        except errors.Error as err:
            logger.error(
                "creation of tab({}) inside spreadsheet({})  failed with error: {}".format(
                    spreadsheetId, tabTitle, err
                )
            )
            return err
        return result

    # cloning apis
    def copySheetFromSpreadsheetToOtherSpreadsheet(
        self, spreadsheetId, sheetId, destinationSpreadsheetId
    ):
        logger.debug(
            "copySheetFromSpreadsheetToOtherSpreadsheet called with\
                 spreadheetId: {} , sheetId: {} , destinationSpreadsheetId: {}".format(
                spreadsheetId, sheetId, destinationSpreadsheetId
            )
        )
        body = {
            "destination_spreadsheet_id": destinationSpreadsheetId,
        }
        try:
            result = (
                self.sheetService.spreadsheets()
                .sheets()
                .copyTo(spreadsheetId=spreadsheetId, sheetId=sheetId, body=body)
                .execute()
            )
        except errors.Error as err:
            logger.error(
                "copySheetFromSpreadsheetToOtherSpreadsheet failed with error: {}".format(
                    err
                )
            )
            return err
        return result

    def cloneSpreadsheet(self, spreadsheetId, newSpreadsheetTitle, parentFolderId):
        logger.debug(
            "cloneSpreadsheet called with spreadsheetId:{} , newSpreadsheetTitle: {},parentFolderId: {}".format(
                spreadsheetId, newSpreadsheetTitle, parentFolderId
            )
        )
        copied_file = {
            "title": newSpreadsheetTitle,
            "parents": [{"id": parentFolderId}],
        }
        try:
            result = (
                self.gdriveService.files()
                .copy(fileId=spreadsheetId, body=copied_file)
                .execute()
            )
        except errors.Error as err:
            logger.error("cloneSpreadsheet failed with error: {}".format(err))
            return err
        return result

    # deleting apis
    def clearValuesFromSpreadsheet(self, spreadsheetId, requestBody):
        logger.debug(
            "clearValuesFromSpreadsheet called with spreadsheetId: {}, requestbody: {}".format(
                spreadsheetId, requestBody
            )
        )
        try:
            result = (
                self.sheetService.spreadsheets()
                .values()
                .clear(spreadsheetId=spreadsheetId, range=requestBody)
                .execute()
            )
        except errors.Error as err:
            logger.error("clearValuesFromSpreadsheet failed with error: {}".format(err))
            return err
        return result

    def deleteTabFromSpreadsheet(self, spreadsheetId, sheetName):
        logger.debug(
            "deleteTabFromSpreadsheet called with spreadsheetId: {}, sheetName: {}".format(
                spreadsheetId, sheetName
            )
        )
        body = {"requests": [{"deleteSheet": {"sheetId": sheetName}}]}
        try:
            result = (
                self.sheetService.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheetId, body=body)
                .execute()
            )
        except errors.Error as err:
            logger.error("deleteTabFromSpreadsheet failed with error: {}".format(err))
            return err
        return result

    def deleteSpreadsheet(self, spreadsheetId):
        logger.debug(
            "deleteSpreadsheet called with spreadsheetId: {}".format(spreadsheetId)
        )
        try:
            result = self.gdriveService.files().delete(fileId=spreadsheetId).execute()
        except errors.Error as err:
            logger.error("deleteSpreadsheet failed with error: {}".format(err))
            return err
        return result

    # fetching apis

    def getSpreadsheetInfo(self, spreadsheetId):
        logger.debug(
            "getSpreadsheetInfo called with spreadsheetId: {}".format(spreadsheetId)
        )
        try:
            spreadsheet = (
                self.sheetService.spreadsheets()
                .get(spreadsheetId=spreadsheetId)
                .execute()
            )
            result = {}
            result["spreadsheetId"] = spreadsheet["spreadsheetId"]
            result["title"] = spreadsheet["properties"]["title"]
            result["sheets"] = spreadsheet["sheets"]
        except errors.Error as err:
            logger.error("getSpreadsheetInfo failed with error: {}".format(err))
            return err
        return result

    def getSpreadsheetData(self, spreadsheetId, sheets):
        logger.debug(
            "getSpreadsheetData called with spreadsheetId: {}, sheets: {}".format(
                spreadsheetId, sheets
            )
        )
        result = {}
        for sheet in sheets:
            res = self.getSheetData(spreadsheetId=spreadsheetId, sheetName=sheet)
            if type(res) is errors.Error:
                return res
            else:
                result[sheet] = res
        return result

    def getSheetData(self, spreadsheetId, sheetName):
        logger.debug(
            "getSheetData called with spreadsheetId: {}, sheet: {}".format(
                spreadsheetId, sheetName
            )
        )
        try:
            result = (
                self.sheetService.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheetId, range=sheetName)
                .execute()["values"]
            )
        except errors.Error as err:
            logger.error("getSheetData failed with error : {}".format(err))
            return err
        return result

    def getAllSpreadsheetInfo(self):
        logger.debug("getAllSpreadsheetInfo called")
        result = []
        page_token = None
        while True:
            try:
                response = (
                    self.gdriveService.files()
                    .list(
                        q="mimeType='application/vnd.google-apps.spreadsheet'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
            except errors.Error as err:
                logger.error("getAllSpreadsheetInfo failed with error: {}".format(err))
                return err
            for file in response.get("files", []):
                # Process change
                result.append([{"title": file.get("name"), "id": file.get("id")}])
                print("Found file: %s (%s)" % (file.get("name"), file.get("id")))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        return result

    def getLastModifiedTimeOfSpreadsheet(self, spreadsheetId):
        logger.debug(
            "getLastModifiedTimeOfSpreadsheet called with spreadsheetId: {}".format(
                spreadsheetId
            )
        )
        result = {}
        try:
            file = self.gdriveService.files().get(fileId=spreadsheetId).execute()
            result["id"] = file["id"]
            result["title"] = file["title"]
            result["lastModified"] = file["modifiedDate"]
        except errors.Error as err:
            logger.error(
                "getLastModifiedTimeOfSpreadsheet failed with error: {}".format(err)
            )
            return err
        return result

    # renaming apis

    def renameSheet(self, spreadsheetId, sheetId, newTitle):
        logger.debug(
            "renameSheet called with spreadsheetId: {}, sheetId: {}, newTitle: {}".format(
                spreadsheetId, sheetId, newTitle
            )
        )
        body = {
            "requests": (
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": sheetId,
                            "title": newTitle,
                        },
                        "fields": "title",
                    }
                }
            )
        }
        try:
            result = (
                self.sheetService.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheetId, body=body)
                .execute()
            )
        except errors.Error as err:
            logger.debug("renameSheet failed with error: {}".format(err))
            return err
        return result

    def renameSpreadsheet(self, spreadsheetId, newTitle):
        logger.debug(
            "renameSpreadsheet called with spreadsheetId: {}, newTitle: {}".format(
                spreadsheetId, newTitle
            )
        )
        body = {"title": newTitle}
        try:
            result = (
                self.gdriveService.files()
                .patch(fileId=spreadsheetId, body=body, fields="title")
                .execute()
            )
        except errors.Error as err:
            logger.error("renameSpreadsheet failed with error: {}".format(err))
            return err
        return result

    def batchUpdateValues(self, spreadsheetId, requestBody):
        logger.debug(
            "batchUpdateValues called with spreadsheetId: {}, requestBody: {}".format(
                spreadsheetId, requestBody
            )
        )
        try:
            result = (
                self.sheetService.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheetId, body=requestBody)
                .execute()
            )
        except errors.Error as err:
            logger.error("batchUpdateValues failed with error: {}".format(err))
            return err
        return result

    def updateValues(self, spreadsheetId, requestBody):
        logger.debug(
            "updateValues called with spreadsheetId: {}, requestBody: {}".format(
                spreadsheetId, requestBody
            )
        )
        try:
            result = (
                self.sheetService.spreadsheets()
                .update(spreadsheetId, body=requestBody)
                .execute()
            )
        except errors.Error as err:
            logger.error("updateValues failed with error : {}".format(err))
            return err
        return result

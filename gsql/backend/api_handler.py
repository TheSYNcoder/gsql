from googleapiclient import errors
from googleapiclient.discovery import build
from gsql.logging import logger


class ApiHandler:
    def __init__(self, creds) -> None:
        """
        Constructor to build the service objects for handling apis
        """
        self.creds = creds
        #    create service objects for google drive and sheets to access client apis
        try:
            self.gdriveService = build(
                serviceName="drive", version="v3", credentials=self.creds
            )
            self.sheetService = build(
                serviceName="sheets", version="v4", credentials=self.creds
            )
        except errors.Error as err:
            logger.error("driver creation failed with error: {}".format(err))

    #    creation apis
    def createSpreadsheet(self, spreadsheetTitle):
        """
        spreadsheetTitle -> title of new spreadsheet as string
        return -> id of new spreadsheet as string
        """
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
                "creation of spreadsheet with title({}) failed with error: {}".format(
                    spreadsheetTitle, err
                )
            )
            return err
        return spreadsheet.get("spreadsheetId")

    # return sheetId else error
    def createTabInsideSpreadsheet(self, spreadsheetId, tabTitle):
        """
        spreadsheetTitle -> id of spreadsheet as string
        tabTitle -> title of new sheet as sting
        return -> id of new sheet as string
        """
        logger.debug(
            "createTabInsideSpreadsheet called with spreadheetId: {}, tabTitle: {}".format(
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
                    tabTitle, spreadsheetId, err
                )
            )
            return err
        return result.get("replies")[0].get("addSheet").get("properties").get("sheetId")

    # cloning apis
    def copySheetFromSpreadsheetToOtherSpreadsheet(
        self, spreadsheetId, sheetId, destinationSpreadsheetId
    ):
        """
        spreadsheetId -> id of origin spreadsheet as string
        sheetId -> id of sheet to be copied as string
        destinationSpreadsheetId -> id of destination spreadsheet as string
        return -> dict with title and sheetId of new sheet
        """
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
        return {"sheetId": result.get("sheetId"), "title": result.get("title")}

    def cloneSpreadsheet(self, spreadsheetId, newSpreadsheetTitle):
        """
        spreadsheetId -> id of spreadsheet to be cloned as string
        newSpreadsheetTitle -> title for new cloned spreadsheet as string
        return -> id of new cloned spreadsheet as string
        """
        logger.debug(
            "cloneSpreadsheet called with spreadsheetId: {} , newSpreadsheetTitle: {}".format(
                spreadsheetId, newSpreadsheetTitle
            )
        )
        copied_file = {
            "title": newSpreadsheetTitle,
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
        return {"id": result.get("id")}

    # deleting apis
    def clearValuesFromSpreadsheet(self, spreadsheetId, range):
        """
        spreadsheetId -> id of spreadsheet as string
        range -> range of values to be cleared as string ( ex - 'sheet_name!A1:H8'
        to clear values inside a sheet and 'sheet_name' to clear a whole sheet')
        return -> dict of spreadsheetId and clearedRange as string
        """
        logger.debug(
            "clearValuesFromSpreadsheet called with spreadsheetId: {}, range: {}".format(
                spreadsheetId, range
            )
        )
        try:
            result = (
                self.sheetService.spreadsheets()
                .values()
                .clear(spreadsheetId=spreadsheetId, range=range)
                .execute()
            )
        except errors.Error as err:
            logger.error("clearValuesFromSpreadsheet failed with error: {}".format(err))
            return err
        return result

    def deleteTabFromSpreadsheet(self, spreadsheetId, sheetId):
        """
        spreadsheetId -> id of spreadsheet as string
        sheetId -> id of sheet to be deleted as string
        return -> dict of spreadsheetId as string and replies as [{}]
        """
        logger.debug(
            "deleteTabFromSpreadsheet called with spreadsheetId: {}, sheetId: {}".format(
                spreadsheetId, sheetId
            )
        )
        body = {"requests": [{"deleteSheet": {"sheetId": sheetId}}]}
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
        """
        spreadsheedId -> id of spreadsheet to be deleted as string
        return -> empty string
        """
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
        """
        spreadsheetId -> id of spreadsheet as string
        return -> dict of spreadsheetId as string, title as string and sheets as array of dict
        (properties:{title,id,...})
        """
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
        """
        spreadsheetId -> id of spreadsheet as string
        sheets -> list of sheet names(as string)
        return -> dict of sheetName:2-d list(refer to getSheetData)
        """
        logger.debug(
            "getSpreadsheetData called with spreadsheetId: {}, sheets: {}".format(
                spreadsheetId, sheets
            )
        )
        result = {}
        for sheet in sheets:
            res = self.getSheetData(spreadsheetId=spreadsheetId, sheetName=sheet)
            if type(res) is errors.Error or type(res) is Exception:
                return res
            else:
                result[sheet] = res
        return result

    def getSheetData(self, spreadsheetId, sheetName):
        """
        spreadsheetId -> id of spreadsheet as string
        sheetName -> name of sheet as string
        return -> 2-d list of values
        """
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
                .execute()
            )
        except errors.Error as err:
            logger.error("getSheetData failed with error : {}".format(err))
            return err
        if "values" in result.keys():
            return result["values"]
        else:
            return [[]]

    def getAllSpreadsheetInfo(self):
        """
        return -> list of dict with title and id of spreadsheets as string
        """
        logger.debug("getAllSpreadsheetInfo called")
        result = []
        page_token = None
        while True:
            try:
                response = (
                    self.gdriveService.files()
                    .list(
                        q="mimeType='application/vnd.google-apps.spreadsheet'",
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
                result.append({"title": file.get("name"), "id": file.get("id")})
                logger.debug("Found file: %s (%s)" % (file.get("name"), file.get("id")))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        return result

    def getLastModifiedTimeOfSpreadsheet(self, spreadsheetId):
        """
        spreadsheetId -> id of spreadsheet as id
        return -> dict with id , title and modifiedTime as strings
        """
        logger.debug(
            "getLastModifiedTimeOfSpreadsheet called with spreadsheetId: {}".format(
                spreadsheetId
            )
        )
        result = {}
        try:
            file = (
                self.gdriveService.files()
                .get(fileId=spreadsheetId, fields="*")
                .execute()
            )
            result["id"] = file["id"]
            result["title"] = file["name"]
            result["modifiedTime"] = file["modifiedTime"]
        except errors.Error as err:
            logger.error(
                "getLastModifiedTimeOfSpreadsheet failed with error: {}".format(err)
            )
            return err
        return result

    # renaming apis

    def renameSheet(self, spreadsheetId, sheetId, newTitle):
        """
        spreadsheetId -> id of spreadsheet as string
        sheetId -> id of sheet as string
        newTitle -> new title of sheet as string
        return -> dict of spreadsheetId as string and replies as [{}]
        """
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
        """
        spreadsheetId -> id so spreadsheet as string
        newTitle -> new title for spreadsheet as string
        return -> dict with kind(=drive#file),id(of file) as string ,\
         name(new name of file) as string and mimeType as string
        """
        logger.debug(
            "renameSpreadsheet called with spreadsheetId: {}, newTitle: {}".format(
                spreadsheetId, newTitle
            )
        )
        body = {"name": newTitle}
        try:
            result = (
                self.gdriveService.files()
                .update(fileId=spreadsheetId, body=body)
                .execute()
            )
        except errors.Error as err:
            logger.error("renameSpreadsheet failed with error: {}".format(err))
            return err
        return result

    def findAndReplace(self, spreadsheetId, requestBody):
        """
        spreadsheetId -> id of spreadsheet as string
        requestBody -> {
            'findReplace': {
                'find': find,
                'replacement': replacement,
                'allSheets': True or 'sheetId':sheet_id
            }
            since it is batch update then multiple find and replace can be appended as list
        return -> dict with spreadsheetId as string and replies as list of batch updates done as
        [{'findReplace': {'valuesChanged': 1, 'rowsChanged': 1, 'sheetsChanged': 1, 'occurrencesChanged': 1}}]
        }
        """
        logger.debug(
            "findAndReplace called with spreadsheetId: {}, requestBody: {}".format(
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
            logger.error("findAndReplace failed with error: {}".format(err))
            return err
        return result

    def updateValues(self, spreadsheetId, values, range):
        """
        spreadsheetId -> id of spreadsheet as string
        values -> 2-d list of values
        range -> range of values to be updated as string ( ex - 'sheet_name!A1:H8'
        to update all values inside a sheet and 'sheet_name' to update a whole sheet')
        return -> dict : {
            "spreadsheetId": "sampleId",
            "updatedRange": "sampleRange",
            "updatedCells": "sampleCells",
        }
        """
        logger.debug(
            "updateValues called with spreadsheetId: {}, values: {}, range:{}".format(
                spreadsheetId, values, range
            )
        )
        body = {"values": values}
        try:
            result = (
                self.sheetService.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheetId,
                    body=body,
                    range=range,
                    valueInputOption="RAW",
                )
                .execute()
            )
        except errors.Error as err:
            logger.error("updateValues failed with error : {}".format(err))
            return err
        return result

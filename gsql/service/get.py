def getSpreadsheetInfo(service, spreadsheetId):
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    result = {}
    result["spreadsheetId"] = spreadsheet["spreadsheetId"]
    result["title"] = spreadsheet["properties"]["title"]
    result["sheets"] = spreadsheet["sheets"]
    return result


def getSpreadsheetData(service, spreadsheetId, sheets):
    result = {}
    for sheet in sheets:
        result[sheet] = getSheetData(
            service=service, spreadsheetId=spreadsheetId, sheetName=sheet
        )
    return result


def getSheetData(service, spreadsheetId, sheetName):
    spreadsheet = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheetId, range=sheetName)
        .execute()
    )
    return spreadsheet["values"]


def getAllSpreadsheetInfo(service):
    result = []
    page_token = None
    while True:
        response = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.spreadsheet'",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
            )
            .execute()
        )
        for file in response.get("files", []):
            # Process change
            result.append([{"title": file.get("name"), "id": file.get("id")}])
            print("Found file: %s (%s)" % (file.get("name"), file.get("id")))
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break

    return result


def getLastModifiedTimeOfSpreadsheet(service, spreadsheetId):
    file = service.files().get(fileId=spreadsheetId).execute()
    result = {}
    result["id"] = file["id"]
    result["title"] = file["title"]
    result["lastModified"] = file["modifiedDate"]
    return result

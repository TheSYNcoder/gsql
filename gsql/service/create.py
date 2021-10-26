def createSpreadsheet(service, sheetTitle):
    spreadsheet = {"properties": {"title": sheetTitle}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
    print("Spreadsheet ID: {0}".format(spreadsheet.get("spreadsheetId")))
    return spreadsheet.get("spreadsheetId")


def createTabInsideSpreadsheet(service, spreadsheetId, tabTitle):
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
    result = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheetId, body=body)
        .execute()
    )
    return result

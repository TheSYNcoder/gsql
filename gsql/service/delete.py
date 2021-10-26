def clearValuesFromSpreadsheet(service, spreadsheetId, requestBody):
    result = (
        service.spreadsheets()
        .values()
        .clear(spreadsheetId=spreadsheetId, range=requestBody)
        .execute()
    )
    return result


def deleteTabFromSpreadsheet(service, spreadsheetId, sheetName):
    body = {"requests": [{"deleteSheet": {"sheetId": sheetName}}]}
    result = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheetId, body=body)
        .execute()
    )
    return result


def deleteSpreadsheet(service, spreadsheetId):
    result = service.files().delete(fileId=spreadsheetId).execute()
    return result

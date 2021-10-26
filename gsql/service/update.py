def batchUpdateValues(service, spreadsheetId, requestBody):
    result = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheetId, body=requestBody)
        .execute()
    )
    return result


def updateValues(service, spreadsheetId, requestBody):
    result = service.spreadsheets().update(spreadsheetId, body=requestBody).execute()
    return result

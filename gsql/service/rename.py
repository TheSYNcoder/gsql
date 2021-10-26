def renameSheet(service, spreadsheetId, sheetId, newTitle):
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
    result = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheetId, body=body)
        .execute()
    )
    return result


def renameSpreadsheet(service, spreadsheetId, newTitle):
    body = {"title": newTitle}
    result = (
        service.files().patch(fileId=spreadsheetId, body=body, fields="title").execute()
    )
    return result

def copySheetFromSpreadsheetToOtherSpreadsheet(
    service, spreadsheetId, sheetId, destinationSpreadsheetId
):
    body = {
        "destination_spreadsheet_id": destinationSpreadsheetId,
    }
    result = (
        service.spreadsheets()
        .sheets()
        .copyTo(spreadsheetId=spreadsheetId, sheetId=sheetId, body=body)
        .execute()
    )
    return result


def cloneSpreadsheet(service, spreadsheetId, newSpreadsheetTitle, parentFolderId):
    copied_file = {"title": newSpreadsheetTitle, "parents": [{"id": parentFolderId}]}
    result = service.files().copy(fileId=spreadsheetId, body=copied_file).execute()
    return result

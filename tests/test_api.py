from gsql.backend import api_handler
from googleapiclient import errors


def test_init_success(monkeypatch, caplog):
    def mock_build_success(*args, **kwargs):
        return "mock_build_obj"

    monkeypatch.setattr(api_handler, "build", mock_build_success)
    instance = api_handler.ApiHandler("creds")
    assert instance.creds == "creds"
    assert instance.gdriveService == "mock_build_obj"
    assert instance.sheetService == "mock_build_obj"


def test_init_failure_error(monkeypatch, mocker, caplog):
    def mock_build_failure(*args, **kwargs):
        raise errors.Error("invalid cred error")

    monkeypatch.setattr(api_handler, "build", mock_build_failure)
    instance = api_handler.ApiHandler("creds")
    assert instance.creds == "creds"
    assert (
        caplog.records[0].msg == "driver creation failed with error: invalid cred error"
    )


class BaseMockSpreadSheetDriveService:
    """
    Base class to mock service objects
    """

    def __init__(self) -> None:
        self.mock_spreadsheet = None

    def values(self, *args, **kwargs):
        return self

    def create(self, *args, **kwargs):
        return self

    def batchUpdate(self, *args, **kwargs):
        return self

    def update(self, *args, **kwargs):
        return self

    def clear(self, *args, **kwargs):
        return self

    def list(self, *args, **kwargs):
        return self

    def copy(self, *args, **kwargs):
        return self

    def copyTo(self, *args, **kwargs):
        return self

    def delete(self, *args, **kwargs):
        return self

    def get(self, *args, **kwargs):
        return self

    def spreadsheets(self, *args, **kwargs):
        return self

    def files(self, *args, **kwargs):
        return self

    def sheets(self, *args, **kwargs):
        return self


class MockSpreadSheetDriveServiceSuccess(BaseMockSpreadSheetDriveService):
    def execute(self, *args, **kwargs):
        return self.mock_spreadsheet


class MockSpreadSheetDriveServiceError(BaseMockSpreadSheetDriveService):
    def execute(self, *args, **kwargs):
        raise errors.Error("error")


def test_create_spreadsheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleid",
            "spreadSheetTitle": "sampleTitle",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    spreadsheetId = instance.createSpreadsheet("sampleId")
    assert spreadsheetId == "sampleid"
    assert caplog.records[0].msg == "createSpreadsheet called with sheetTitle: sampleId"


def test_create_spreadsheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleid",
            "spreadSheetTitle": "sampleTitle",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.createSpreadsheet("sampleId")
    assert caplog.records[0].msg == "createSpreadsheet called with sheetTitle: sampleId"
    assert (
        caplog.records[1].msg
        == "creation of spreadsheet with title(sampleId) failed with error: error"
    )


def test_add_sheet_success(monkeypatch, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleid",
            "replies": [{"addSheet": {"properties": {"sheetId": "sampleId"}}}],
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheetId = instance.createTabInsideSpreadsheet("sampleId", "sampleTitle")
    assert sheetId == "sampleId"
    assert (
        caplog.records[0].msg
        == "createTabInsideSpreadsheet called with spreadheetId: sampleId, tabTitle: sampleTitle"
    )


def test_add_sheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleid",
            "replies": [{"addSheet": {"properties": {"sheetId": "sampleId"}}}],
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.createTabInsideSpreadsheet("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "createTabInsideSpreadsheet called with spreadheetId: sampleId, tabTitle: sampleTitle"
    )
    assert (
        caplog.records[1].msg
        == "creation of tab(sampleTitle) inside spreadsheet(sampleId)  failed with error: error"
    )


def test_copy_sheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {"sheetId": "sampleId", "title": "sampleTitle"}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.copySheetFromSpreadsheetToOtherSpreadsheet(
        "sampleId", "sampleId", "sampleId"
    )
    assert sheet.get("sheetId") == "sampleId"
    assert sheet.get("title") == "sampleTitle"
    assert (
        caplog.records[0].msg
        == "copySheetFromSpreadsheetToOtherSpreadsheet called with\
                 spreadheetId: sampleId , sheetId: sampleId , destinationSpreadsheetId: sampleId"
    )


def test_copy_sheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {"sheetId": "sampleId", "title": "sampleTitle"}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.copySheetFromSpreadsheetToOtherSpreadsheet(
        "sampleId", "sampleId", "sampleId"
    )
    assert (
        caplog.records[0].msg
        == "copySheetFromSpreadsheetToOtherSpreadsheet called with\
                 spreadheetId: sampleId , sheetId: sampleId , destinationSpreadsheetId: sampleId"
    )
    assert (
        caplog.records[1].msg
        == "copySheetFromSpreadsheetToOtherSpreadsheet failed with error: error"
    )


def test_clone_spreadsheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "id": "sampleId",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.cloneSpreadsheet("sampleId", "sampleTitle")
    assert sheet.get("id") == "sampleId"
    assert (
        caplog.records[0].msg
        == "cloneSpreadsheet called with spreadsheetId: sampleId , newSpreadsheetTitle: sampleTitle"
    )


def test_clone_spreadsheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "id": "sampleId",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.cloneSpreadsheet("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "cloneSpreadsheet called with spreadsheetId: sampleId , newSpreadsheetTitle: sampleTitle"
    )
    assert caplog.records[1].msg == "cloneSpreadsheet failed with error: error"


def test_clear_values_spreadsheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "clearedRange": "sampleRange",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.clearValuesFromSpreadsheet("sampleId", "sampleRange")
    assert sheet.get("spreadsheetId") == "sampleId"
    assert sheet.get("clearedRange") == "sampleRange"
    assert (
        caplog.records[0].msg
        == "clearValuesFromSpreadsheet called with spreadsheetId: sampleId, range: sampleRange"
    )


def test_clear_values_spreadsheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "clearedRange": "sampleRange",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.clearValuesFromSpreadsheet("sampleId", "sampleRange")
    assert (
        caplog.records[0].msg
        == "clearValuesFromSpreadsheet called with spreadsheetId: sampleId, range: sampleRange"
    )
    assert (
        caplog.records[1].msg == "clearValuesFromSpreadsheet failed with error: error"
    )


def test_delete_tab_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {"spreadsheetId": "sampleId", "replies": [{}]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.deleteTabFromSpreadsheet("sampleId", "sampleId")
    assert sheet.get("spreadsheetId") == "sampleId"
    assert sheet.get("replies") == [{}]
    assert (
        caplog.records[0].msg
        == "deleteTabFromSpreadsheet called with spreadsheetId: sampleId, sheetId: sampleId"
    )


def test_delete_tab_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {"spreadsheetId": "sampleId", "replies": [{}]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.deleteTabFromSpreadsheet("sampleId", "sampleId")
    assert (
        caplog.records[0].msg
        == "deleteTabFromSpreadsheet called with spreadsheetId: sampleId, sheetId: sampleId"
    )
    assert caplog.records[1].msg == "deleteTabFromSpreadsheet failed with error: error"


def test_delete_spreadsheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = ""
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.deleteSpreadsheet("sampleId")
    assert sheet == ""
    assert (
        caplog.records[0].msg == "deleteSpreadsheet called with spreadsheetId: sampleId"
    )


def test_delete_spreadsheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = ""
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.deleteSpreadsheet("sampleId")
    assert (
        caplog.records[0].msg == "deleteSpreadsheet called with spreadsheetId: sampleId"
    )
    assert caplog.records[1].msg == "deleteSpreadsheet failed with error: error"


def test_get_spreadsheet_info_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "properties": {"title": "title"},
            "sheets": "sheets",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.getSpreadsheetInfo("sampleId")
    assert sheet.get("spreadsheetId") == "sampleId"
    assert sheet.get("title") == "title"
    assert sheet.get("sheets") == "sheets"
    assert (
        caplog.records[0].msg
        == "getSpreadsheetInfo called with spreadsheetId: sampleId"
    )


def test_get_spreadsheet_info_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "properties": {"title": "title"},
            "sheets": "sheets",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.getSpreadsheetInfo("sampleId")
    assert (
        caplog.records[0].msg
        == "getSpreadsheetInfo called with spreadsheetId: sampleId"
    )
    assert caplog.records[1].msg == "getSpreadsheetInfo failed with error: error"


def test_get_sheetdata_success_valued(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {"values": [[1, 2], [3, 4]]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.getSheetData("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "getSheetData called with spreadsheetId: sampleId, sheet: sampleTitle"
    )
    assert sheet == [[1, 2], [3, 4]]


def test_get_sheetdata_success_filled(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.getSheetData("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "getSheetData called with spreadsheetId: sampleId, sheet: sampleTitle"
    )
    assert sheet == [[]]


def test_get_sheetdata_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {"values": [[1, 2], [3, 4]]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.getSheetData("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "getSheetData called with spreadsheetId: sampleId, sheet: sampleTitle"
    )
    assert caplog.records[1].msg == "getSheetData failed with error : error"


def test_get_spreadsheet_data_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {"values": [[1, 2], [3, 4]]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    instance.getSheetData = lambda spreadsheetId, sheetName: [[1, 2], [3, 4]]
    spreadsheet = instance.getSpreadsheetData("sampleId", ["sampleTitle"])
    assert caplog.records[
        0
    ].msg == "getSpreadsheetData called with spreadsheetId: sampleId, sheets: {}".format(
        ["sampleTitle"]
    )
    assert spreadsheet.get("sampleTitle") == [[1, 2], [3, 4]]


def test_get_spreadsheet_data_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = BaseMockSpreadSheetDriveService()
        instance.mock_spreadsheet = {"values": [[1, 2], [3, 4]]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    instance.getSheetData = lambda spreadsheetId, sheetName: errors.Error("error")
    spreadsheet = instance.getSpreadsheetData("sampleId", ["sampleTitle"])
    assert caplog.records[
        0
    ].msg == "getSpreadsheetData called with spreadsheetId: sampleId, sheets: {}".format(
        ["sampleTitle"]
    )
    assert type(spreadsheet) == errors.Error


def test_get_all_spreadsheet_info_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "files": [{"name": "sampleTitle", "id": "sampleId"}]
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.getAllSpreadsheetInfo()
    assert caplog.records[0].msg == "getAllSpreadsheetInfo called"
    assert sheet == [{"title": "sampleTitle", "id": "sampleId"}]
    assert caplog.records[1].msg == "Found file: sampleTitle (sampleId)"


def test_get_all_spreadsheet_info_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "files": [{"name": "sampleTitle", "id": "sampleId"}]
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.getAllSpreadsheetInfo()
    assert caplog.records[0].msg == "getAllSpreadsheetInfo called"
    assert caplog.records[1].msg == "getAllSpreadsheetInfo failed with error: error"


def test_get_lastmodifiedtime_spreadsheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "id": "sampleId",
            "name": "sampleName",
            "modifiedTime": "sampleTime",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.getLastModifiedTimeOfSpreadsheet("sampleId")
    assert (
        caplog.records[0].msg
        == "getLastModifiedTimeOfSpreadsheet called with spreadsheetId: sampleId"
    )
    assert sheet == {
        "id": "sampleId",
        "title": "sampleName",
        "modifiedTime": "sampleTime",
    }


def test_get_lastmodifiedtime_spreadsheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "id": "sampleId",
            "name": "sampleName",
            "modifiedTime": "sampleTime",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.getLastModifiedTimeOfSpreadsheet("sampleId")
    assert type(sheet) == errors.Error
    assert (
        caplog.records[0].msg
        == "getLastModifiedTimeOfSpreadsheet called with spreadsheetId: sampleId"
    )
    assert (
        caplog.records[1].msg
        == "getLastModifiedTimeOfSpreadsheet failed with error: error"
    )


def test_rename_sheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {"spreadsheetId": "sampleId", "replies": [{}]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.renameSheet("sampleId", "sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "renameSheet called with spreadsheetId: sampleId, sheetId: sampleId, newTitle: sampleTitle"
    )
    assert sheet == {"spreadsheetId": "sampleId", "replies": [{}]}


def test_rename_sheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {"spreadsheetId": "sampleId", "replies": [{}]}
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.renameSheet("sampleId", "sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "renameSheet called with spreadsheetId: sampleId, sheetId: sampleId, newTitle: sampleTitle"
    )
    assert caplog.records[1].msg == "renameSheet failed with error: error"


def test_rename_spreadsheet_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "kind": "drive#file",
            "id": "sampleId",
            "name": "sampleTitle",
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.renameSpreadsheet("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "renameSpreadsheet called with spreadsheetId: sampleId, newTitle: sampleTitle"
    )
    assert sheet.get("id") == "sampleId"
    assert sheet.get("kind") == "drive#file"
    assert sheet.get("name") == "sampleTitle"


def test_rename_spreadsheet_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "kind": "drive#file",
            "id": "sampleId",
            "name": "sampleTitle",
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.renameSpreadsheet("sampleId", "sampleTitle")
    assert (
        caplog.records[0].msg
        == "renameSpreadsheet called with spreadsheetId: sampleId, newTitle: sampleTitle"
    )
    assert caplog.records[1].msg == "renameSpreadsheet failed with error: error"


def test_find_and_replace_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "replies": [{"findReplace": "sampleRes"}],
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.findAndReplace("sampleId", "sampleBody")
    assert (
        caplog.records[0].msg
        == "findAndReplace called with spreadsheetId: sampleId, requestBody: sampleBody"
    )
    assert sheet.get("spreadsheetId") == "sampleId"
    assert sheet.get("replies")[0].get("findReplace") == "sampleRes"


def test_find_and_replace_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "replies": [{"findReplace": "sampleRes"}],
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.findAndReplace("sampleId", "sampleBody")
    assert (
        caplog.records[0].msg
        == "findAndReplace called with spreadsheetId: sampleId, requestBody: sampleBody"
    )
    assert caplog.records[1].msg == "findAndReplace failed with error: error"
    assert type(sheet) == errors.Error


def test_update_values_success(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceSuccess()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "updatedRange": "sampleRange",
            "updatedCells": "sampleCells",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    sheet = instance.updateValues("sampleId", "sampleValue", "sampleRange")
    assert (
        caplog.records[0].msg
        == "updateValues called with spreadsheetId: sampleId, values: sampleValue, range:sampleRange"
    )
    assert sheet.get("spreadsheetId") == "sampleId"
    assert sheet.get("updatedRange") == "sampleRange"
    assert sheet.get("updatedCells") == "sampleCells"


def test_update_values_fail_error(monkeypatch, mocker, caplog):
    def mock_build_func(*args, **kwargs):
        instance = MockSpreadSheetDriveServiceError()
        instance.mock_spreadsheet = {
            "spreadsheetId": "sampleId",
            "updatedRange": "sampleRange",
            "updatedCells": "sampleCells",
        }
        return instance

    monkeypatch.setattr(api_handler, "build", mock_build_func)
    instance = api_handler.ApiHandler("creds")
    _ = instance.updateValues("sampleId", "sampleValue", "sampleRange")
    assert (
        caplog.records[0].msg
        == "updateValues called with spreadsheetId: sampleId, values: sampleValue, range:sampleRange"
    )
    assert caplog.records[1].msg == "updateValues failed with error : error"

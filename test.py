from gsql.backend.auth import Auth
from gsql.backend.api_handler import ApiHandler

ath = Auth()
ath.auth()
api = ApiHandler(ath.creds)
print(
    api.updateValues(
        "1Kw9pxLKXSza9-h14Ikwk5pPzfBGoJkShaLdxn93YMLc",
        [[1, 2, 3], [3, "hiii", 9]],
        "hello!A1:C2",
    )
)

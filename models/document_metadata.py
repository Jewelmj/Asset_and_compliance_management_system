from datetime import date

class DocumentMetadata:
    """
    Stores metadata about a document:
    - File path
    - Issue and expiry dates
    - Document owner (asset or user)
    """

    def __init__(self, file_path=None, issued_on: date = None, expires_on: date = None):
        self.file_path = file_path
        self.issued_on = issued_on
        self.expires_on = expires_on

    def set_file_path(self, path: str):
        self.file_path = path

    def set_issue_date(self, issued_date: date):
        self.issued_on = issued_date

    def set_expiry_date(self, expiry_date: date):
        self.expires_on = expiry_date
from datetime import datetime


class DocumentHistory:
    """
    Stores document-related logs such as edits, validations, integrity checks.
    """

    def __init__(self):
        self.events = []

    def log(self, message: str):
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "event": message
        })
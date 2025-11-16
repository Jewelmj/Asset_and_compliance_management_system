from datetime import datetime

class AssetHistory:
    """
    Stores and manages the event history (movements, assignments, etc.)
    """

    def __init__(self):
        self.events = []

    def log(self, message: str):
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "event": message
        })
from datetime import datetime

class PlaceHistory:
    """
    Tracks events or updates related to a place.
    """

    def __init__(self):
        self.events = []

    def log(self, message: str):
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "event": message
        })
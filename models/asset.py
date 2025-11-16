import uuid

class Asset:
    """
    Pure data model representing an asset.
    Contains no assignment or business logic.
    """

    def __init__(self, name: str, category: str, media, history):
        self.asset_id = str(uuid.uuid4())
        self.name = name
        self.category = category

        self.media = media          # AssetMedia instance
        self.history = history      # AssetHistory instance

    def __str__(self):
        return f"Asset(ID={self.asset_id}, Name={self.name}, Category={self.category})"
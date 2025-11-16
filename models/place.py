import uuid
from models.asset_collection import AssetCollection
from models.people_collection import PeopleCollection


class Place:
    """
    Represents a single type of physical location in the system.
    This Place can store assets and people, replacing the old Jobsite class.
    """

    def __init__(self, name, location=None, metadata=None, history=None):
        self.place_id = str(uuid.uuid4())
        self.name = name
        self.location = location
        self.metadata = metadata      # PlaceMetadata instance
        self.history = history        # PlaceHistory instance

        self.assets = AssetCollection()
        self.people = PeopleCollection()

    def __str__(self):
        return (
            f"Place(ID={self.place_id}, Name={self.name}, "
            f"Assets={self.assets.count()}, People={self.people.count()})"
        )
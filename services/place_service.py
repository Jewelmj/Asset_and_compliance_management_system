from models.place import Place
from models.place_metadata import PlaceMetadata
from models.place_history import PlaceHistory

class PlaceService:
    """
    Handles business logic for Place:
    - Creating places
    - Assigning assets and users
    - Updating metadata
    - Logging activities
    """

    def create_place(self, name, location=None, description=None, created_by=None):
        metadata = PlaceMetadata(description=description, created_by=created_by)
        history = PlaceHistory()

        place = Place(name=name, location=location, metadata=metadata, history=history)
        history.log("Place created")

        return place

    def add_asset(self, place, asset):
        place.assets.add(asset)
        place.history.log(f"Asset added: {asset.name}")

    def add_person(self, place, user):
        place.people.add(user)
        place.history.log(f"User added: {user.name}")

    def update_description(self, place, new_desc):
        place.metadata.set_description(new_desc)
        place.history.log(f"Description updated: {new_desc}")
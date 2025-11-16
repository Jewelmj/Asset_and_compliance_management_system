class PlaceMetadata:
    """
    Stores metadata about a place.
    """

    def __init__(self, description=None, created_by=None):
        self.description = description
        self.created_by = created_by

    def set_description(self, desc):
        self.description = desc

    def set_creator(self, creator):
        self.created_by = creator
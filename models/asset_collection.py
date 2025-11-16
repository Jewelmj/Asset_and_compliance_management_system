class AssetCollection:
    """
    A manager for storing and organizing assets inside a place/jobsite.
    """

    def __init__(self):
        self.assets = []

    def add(self, asset):
        if asset not in self.assets:
            self.assets.append(asset)

    def remove(self, asset):
        if asset in self.assets:
            self.assets.remove(asset)

    def list(self):
        return self.assets

    def count(self):
        return len(self.assets)

    def find_by_name(self, name):
        return [a for a in self.assets if a.name == name]
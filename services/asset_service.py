from models.asset import Asset
from models.asset_media import AssetMedia
from models.asset_history import AssetHistory
from services.asset_assigner import AssetAssigner


class AssetService:
    """
    Service/Manager class that handles:
    - Creating an asset
    - Assigning an asset
    - Managing media (photo, QR)
    - Logging actions
    """

    def create_asset(self, name: str, category: str, photo_path: str = None):
        media = AssetMedia(photo_path=photo_path)
        history = AssetHistory()

        asset = Asset(name=name, category=category, media=media, history=history)
        history.log("Asset created")

        return asset

    def assign_to_user(self, asset, user):
        assigner = AssetAssigner(history=asset.history)
        assigner.assign_to_user(user)
        return assigner

    def assign_to_jobsite(self, asset, jobsite):
        assigner = AssetAssigner(history=asset.history)
        assigner.assign_to_jobsite(jobsite)
        return assigner

    def assign_to_vehicle(self, asset, vehicle):
        assigner = AssetAssigner(history=asset.history)
        assigner.assign_to_vehicle(vehicle)
        return assigner

    def set_photo(self, asset, path):
        asset.media.set_photo(path)
        asset.history.log(f"Photo updated: {path}")

    def set_qr_code(self, asset, path):
        asset.media.set_qr(path)
        asset.history.log(f"QR code set: {path}")
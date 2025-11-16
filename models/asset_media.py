class AssetMedia:
    """
    Holds all media-related paths for an asset.
    - Photo path
    - QR code path
    """

    def __init__(self, photo_path=None, qr_code_path=None):
        self.photo_path = photo_path
        self.qr_code_path = qr_code_path

    def set_photo(self, path: str):
        self.photo_path = path

    def set_qr(self, path: str):
        self.qr_code_path = path
from models.asset import Asset
from database.models import AssetORM

class AssetMapper:

    @staticmethod
    def to_orm(domain_asset: Asset) -> AssetORM:
        return AssetORM(
            id=domain_asset.asset_id,
            name=domain_asset.name,
            category=domain_asset.category
        )

    @staticmethod
    def to_domain(asset_orm: AssetORM) -> Asset:
        return Asset(
            name=asset_orm.name,
            category=asset_orm.category,
            media=None,
            history=None
        )

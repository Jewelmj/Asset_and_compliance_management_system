from flask import Blueprint, request
from database.db import SessionLocal
from mappers.asset_mapper import AssetMapper
from models.asset_media import AssetMedia
from models.asset_history import AssetHistory
from models.asset import Asset

assets_bp = Blueprint("assets", __name__)

@assets_bp.post("/")
def create_asset():
    data = request.json
    name = data.get("name")
    category = data.get("category")

    domain_asset = Asset(
        name=name,
        category=category,
        media=AssetMedia(),
        history=AssetHistory(),
    )

    asset_orm = AssetMapper.to_orm(domain_asset)

    db = SessionLocal()
    db.add(asset_orm)
    db.commit()

    return {
        "asset_id": domain_asset.asset_id,
        "name": domain_asset.name,
        "category": domain_asset.category
    }, 201

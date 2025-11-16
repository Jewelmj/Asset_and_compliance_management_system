from flask import Blueprint, request
from services.asset_service import AssetService

assets_bp = Blueprint("assets", __name__)

ASSETS_DB = {}

asset_service = AssetService()


@assets_bp.post("/")
def create_asset():
    data = request.json
    name = data.get("name")
    category = data.get("category")

    asset = asset_service.create_asset(name, category)

    ASSETS_DB[asset.asset_id] = asset

    return {
        "asset_id": asset.asset_id,
        "name": asset.name,
        "category": asset.category
    }, 201


@assets_bp.get("/")
def list_assets():
    return {
        "assets": [
            {
                "asset_id": a.asset_id,
                "name": a.name,
                "category": a.category
            }
            for a in ASSETS_DB.values()
        ]
    }
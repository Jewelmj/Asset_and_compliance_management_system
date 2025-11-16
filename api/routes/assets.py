from flask import Blueprint, request
from database.db import SessionLocal
from database.models import AssetORM
import uuid

assets_bp = Blueprint("assets", __name__)

@assets_bp.post("/")
def create_asset():
    data = request.json
    name = data.get("name")
    category = data.get("category")

    asset_id = str(uuid.uuid4())
    db = SessionLocal()
    asset = AssetORM(id=asset_id, name=name, category=category)

    db.add(asset)
    db.commit()

    return {
        "asset_id": asset.id,
        "name": asset.name,
        "category": asset.category,
    }, 201


@assets_bp.get("/")
def list_assets():
    db = SessionLocal()
    assets = db.query(AssetORM).all()

    return {
        "assets": [
            {
                "asset_id": a.id,
                "name": a.name,
                "category": a.category,
            }
            for a in assets
        ]
    }

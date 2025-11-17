"""
Asset management routes for the Site-Steward API.
Handles asset CRUD operations and movement tracking.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from database.db import get_db
from database.models import AssetORM, ProjectORM, AssetHistoryORM
from api.middleware.auth import jwt_required_custom
import uuid
from datetime import datetime

assets_bp = Blueprint("assets", __name__)


@assets_bp.route("/", methods=["GET"])
@jwt_required_custom()
def list_assets():
    """
    List all assets with their current project information.
    
    Response:
        [
            {
                "id": "asset_id",
                "name": "Asset Name",
                "category": "Category",
                "project_id": "project_id" or null,
                "project_name": "Project Name" or null
            }
        ]
    
    Requirements: 2.5
    """
    try:
        db = next(get_db())
        
        # Query all assets with their project information
        assets = db.query(AssetORM).all()
        
        result = []
        for asset in assets:
            asset_data = {
                "id": asset.id,
                "name": asset.name,
                "category": asset.category,
                "project_id": asset.project_id,
                "project_name": asset.project.name if asset.project else None
            }
            result.append(asset_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@assets_bp.route("/", methods=["POST"])
@jwt_required_custom()
def create_asset():
    """
    Create a new asset.
    
    Request body:
        {
            "name": "Asset Name",
            "category": "Category"
        }
    
    Response:
        {
            "id": "asset_id",
            "name": "Asset Name",
            "category": "Category",
            "qr_code_url": null
        }
    
    Requirements: 2.1
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body is required"
            }), 400
        
        name = data.get("name")
        category = data.get("category")
        
        # Validate input
        if not name or not category:
            return jsonify({
                "error": "Bad Request",
                "message": "Name and category are required"
            }), 400
        
        db = next(get_db())
        
        # Create new asset
        asset_id = str(uuid.uuid4())
        new_asset = AssetORM(
            id=asset_id,
            name=name,
            category=category,
            project_id=None
        )
        
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        
        return jsonify({
            "id": new_asset.id,
            "name": new_asset.name,
            "category": new_asset.category,
            "qr_code_url": None  # QR code generation handled by frontend
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@assets_bp.route("/<asset_id>", methods=["GET"])
@jwt_required_custom()
def get_asset_details(asset_id):
    """
    Get detailed information about a specific asset.
    
    Response:
        {
            "id": "asset_id",
            "name": "Asset Name",
            "category": "Category",
            "project_id": "project_id" or null,
            "project_name": "Project Name" or null,
            "history": [
                {
                    "id": "history_id",
                    "project_id": "project_id",
                    "project_name": "Project Name",
                    "moved_at": "2024-01-01T12:00:00",
                    "moved_by": "user_id"
                }
            ]
        }
    
    Requirements: 2.3
    """
    try:
        db = next(get_db())
        
        # Query asset by ID
        asset = db.query(AssetORM).filter(AssetORM.id == asset_id).first()
        
        if not asset:
            return jsonify({
                "error": "Not Found",
                "message": f"Asset with ID {asset_id} not found"
            }), 404
        
        # Get asset history
        history_records = db.query(AssetHistoryORM).filter(
            AssetHistoryORM.asset_id == asset_id
        ).order_by(AssetHistoryORM.moved_at.desc()).all()
        
        history = []
        for record in history_records:
            history.append({
                "id": record.id,
                "project_id": record.project_id,
                "project_name": record.project.name if record.project else None,
                "moved_at": record.moved_at.isoformat() if record.moved_at else None,
                "moved_by": record.moved_by
            })
        
        result = {
            "id": asset.id,
            "name": asset.name,
            "category": asset.category,
            "project_id": asset.project_id,
            "project_name": asset.project.name if asset.project else None,
            "history": history
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@assets_bp.route("/<asset_id>/move", methods=["POST"])
@jwt_required_custom()
def move_asset(asset_id):
    """
    Move an asset to a different project.
    
    Request body:
        {
            "project_id": "project_id"
        }
    
    Response:
        {
            "success": true,
            "message": "Asset moved successfully"
        }
    
    Requirements: 2.4, 2.5
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body is required"
            }), 400
        
        project_id = data.get("project_id")
        
        if not project_id:
            return jsonify({
                "error": "Bad Request",
                "message": "project_id is required"
            }), 400
        
        db = next(get_db())
        
        # Verify asset exists
        asset = db.query(AssetORM).filter(AssetORM.id == asset_id).first()
        if not asset:
            return jsonify({
                "error": "Not Found",
                "message": f"Asset with ID {asset_id} not found"
            }), 404
        
        # Verify project exists
        project = db.query(ProjectORM).filter(ProjectORM.id == project_id).first()
        if not project:
            return jsonify({
                "error": "Not Found",
                "message": f"Project with ID {project_id} not found"
            }), 404
        
        # Get current user ID from JWT
        user_id = get_jwt_identity()
        
        # Create history record before updating asset
        history_id = str(uuid.uuid4())
        history_record = AssetHistoryORM(
            id=history_id,
            asset_id=asset_id,
            project_id=project_id,
            moved_by=user_id,
            moved_at=datetime.utcnow()
        )
        
        # Update asset location
        asset.project_id = project_id
        
        db.add(history_record)
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "Asset moved successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

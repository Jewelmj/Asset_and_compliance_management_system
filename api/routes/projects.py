"""
Project management routes for the Site-Steward API.
Handles project CRUD operations and compliance status.
"""
from flask import Blueprint, request, jsonify
from database.db import get_db
from database.models import ProjectORM, AssetORM, SubcontractorORM, ComplianceDocumentORM
from api.middleware.auth import jwt_required_custom
import uuid
from datetime import datetime, timedelta

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/", methods=["GET"])
@jwt_required_custom()
def list_projects():
    """
    List all projects with asset count.
    
    Response:
        [
            {
                "id": "project_id",
                "name": "Project Name",
                "location": "Location",
                "asset_count": 5
            }
        ]
    
    Requirements: 3.1
    """
    try:
        db = next(get_db())
        
        # Query all projects
        projects = db.query(ProjectORM).all()
        
        result = []
        for project in projects:
            project_data = {
                "id": project.id,
                "name": project.name,
                "location": project.location,
                "asset_count": len(project.assets)
            }
            result.append(project_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@projects_bp.route("/", methods=["POST"])
@jwt_required_custom()
def create_project():
    """
    Create a new project.
    
    Request body:
        {
            "name": "Project Name",
            "location": "Location"
        }
    
    Response:
        {
            "id": "project_id",
            "name": "Project Name",
            "location": "Location"
        }
    
    Requirements: 3.1
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body is required"
            }), 400
        
        name = data.get("name")
        location = data.get("location")
        
        # Validate input
        if not name:
            return jsonify({
                "error": "Bad Request",
                "message": "Name is required"
            }), 400
        
        db = next(get_db())
        
        # Create new project
        project_id = str(uuid.uuid4())
        new_project = ProjectORM(
            id=project_id,
            name=name,
            location=location
        )
        
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        
        return jsonify({
            "id": new_project.id,
            "name": new_project.name,
            "location": new_project.location
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500



@projects_bp.route("/<project_id>/compliance", methods=["GET"])
@jwt_required_custom()
def get_project_compliance(project_id):
    """
    Get compliance status for all subcontractors on a project.
    
    Response:
        {
            "project_id": "project_id",
            "subcontractors": [
                {
                    "id": "subcontractor_id",
                    "name": "Subcontractor Name",
                    "status": "RED" or "GREEN",
                    "documents": [
                        {
                            "id": "document_id",
                            "document_type": "Insurance",
                            "expiry_date": "2024-12-31",
                            "status": "RED" or "GREEN"
                        }
                    ]
                }
            ]
        }
    
    Requirements: 3.3, 3.4, 5.3, 5.4
    """
    try:
        db = next(get_db())
        
        # Verify project exists
        project = db.query(ProjectORM).filter(ProjectORM.id == project_id).first()
        if not project:
            return jsonify({
                "error": "Not Found",
                "message": f"Project with ID {project_id} not found"
            }), 404
        
        # Import compliance service
        from services.compliance_service import ComplianceService
        
        # Get all subcontractors for this project
        subcontractors_data = []
        for subcontractor in project.subcontractors:
            # Get all documents for this subcontractor
            documents_data = []
            for doc in subcontractor.documents:
                doc_status = ComplianceService.calculate_status(doc.expiry_date)
                documents_data.append({
                    "id": doc.id,
                    "document_type": doc.document_type,
                    "expiry_date": doc.expiry_date.isoformat() if doc.expiry_date else None,
                    "status": doc_status
                })
            
            # Calculate overall subcontractor status
            overall_status = ComplianceService.calculate_subcontractor_status(subcontractor.documents)
            
            subcontractors_data.append({
                "id": subcontractor.id,
                "name": subcontractor.name,
                "status": overall_status,
                "documents": documents_data
            })
        
        result = {
            "project_id": project.id,
            "subcontractors": subcontractors_data
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

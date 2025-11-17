"""
Subcontractor management routes for the Site-Steward API.
Handles subcontractor CRUD operations and compliance document uploads.
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from database.db import get_db
from database.models import SubcontractorORM, ComplianceDocumentORM
from api.middleware.auth import jwt_required_custom
import uuid
import os
from datetime import datetime

subcontractors_bp = Blueprint("subcontractors", __name__)

# Configuration for file uploads
UPLOAD_FOLDER = "uploads/compliance"
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    """Check if file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@subcontractors_bp.route("/", methods=["GET"])
@jwt_required_custom()
def list_subcontractors():
    """
    List all subcontractors.
    
    Response:
        [
            {
                "id": "subcontractor_id",
                "name": "Subcontractor Name",
                "email": "email@example.com",
                "phone": "123-456-7890"
            }
        ]
    
    Requirements: 4.1, 4.4
    """
    try:
        db = next(get_db())
        
        # Query all subcontractors
        subcontractors = db.query(SubcontractorORM).all()
        
        result = []
        for subcontractor in subcontractors:
            subcontractor_data = {
                "id": subcontractor.id,
                "name": subcontractor.name,
                "email": subcontractor.email,
                "phone": subcontractor.phone
            }
            result.append(subcontractor_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@subcontractors_bp.route("/", methods=["POST"])
@jwt_required_custom()
def create_subcontractor():
    """
    Create a new subcontractor.
    
    Request body:
        {
            "name": "Subcontractor Name",
            "email": "email@example.com",
            "phone": "123-456-7890"
        }
    
    Response:
        {
            "id": "subcontractor_id",
            "name": "Subcontractor Name",
            "email": "email@example.com",
            "phone": "123-456-7890"
        }
    
    Requirements: 4.1
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body is required"
            }), 400
        
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        
        # Validate input
        if not name:
            return jsonify({
                "error": "Bad Request",
                "message": "Name is required"
            }), 400
        
        db = next(get_db())
        
        # Create new subcontractor
        subcontractor_id = str(uuid.uuid4())
        new_subcontractor = SubcontractorORM(
            id=subcontractor_id,
            name=name,
            email=email,
            phone=phone
        )
        
        db.add(new_subcontractor)
        db.commit()
        db.refresh(new_subcontractor)
        
        return jsonify({
            "id": new_subcontractor.id,
            "name": new_subcontractor.name,
            "email": new_subcontractor.email,
            "phone": new_subcontractor.phone
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@subcontractors_bp.route("/<sub_id>/document", methods=["POST"])
@jwt_required_custom()
def upload_document(sub_id):
    """
    Upload a compliance document for a subcontractor.
    
    Request: multipart/form-data
        - file: PDF file
        - expiry_date: Date in YYYY-MM-DD format
        - document_type: Type of document (e.g., "Insurance", "Certification")
    
    Response:
        {
            "id": "document_id",
            "file_path": "uploads/compliance/filename.pdf",
            "expiry_date": "2024-12-31",
            "status": "GREEN" or "RED"
        }
    
    Requirements: 4.2, 4.3
    """
    try:
        db = next(get_db())
        
        # Verify subcontractor exists
        subcontractor = db.query(SubcontractorORM).filter(
            SubcontractorORM.id == sub_id
        ).first()
        
        if not subcontractor:
            return jsonify({
                "error": "Not Found",
                "message": f"Subcontractor with ID {sub_id} not found"
            }), 404
        
        # Check if file is present
        if "file" not in request.files:
            return jsonify({
                "error": "Bad Request",
                "message": "No file provided"
            }), 400
        
        file = request.files["file"]
        
        # Check if file is selected
        if file.filename == "":
            return jsonify({
                "error": "Bad Request",
                "message": "No file selected"
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Bad Request",
                "message": "Only PDF files are allowed"
            }), 400
        
        # Validate file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "error": "Bad Request",
                "message": f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024)}MB"
            }), 400
        
        # Get form data
        expiry_date_str = request.form.get("expiry_date")
        document_type = request.form.get("document_type")
        
        if not expiry_date_str or not document_type:
            return jsonify({
                "error": "Bad Request",
                "message": "expiry_date and document_type are required"
            }), 400
        
        # Parse expiry date
        try:
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({
                "error": "Bad Request",
                "message": "expiry_date must be in YYYY-MM-DD format"
            }), 400
        
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Generate secure filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        original_filename = secure_filename(file.filename)
        filename = f"{sub_id}_{document_type}_{timestamp}_{original_filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file
        file.save(file_path)
        
        # Create database record
        document_id = str(uuid.uuid4())
        new_document = ComplianceDocumentORM(
            id=document_id,
            subcontractor_id=sub_id,
            document_type=document_type,
            file_path=file_path,
            expiry_date=expiry_date
        )
        
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        # Calculate status
        from services.compliance_service import ComplianceService
        status = ComplianceService.calculate_status(expiry_date)
        
        return jsonify({
            "id": new_document.id,
            "file_path": new_document.file_path,
            "expiry_date": new_document.expiry_date.isoformat(),
            "status": status
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500

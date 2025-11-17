from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

# Junction table for many-to-many relationship between projects and subcontractors
project_subcontractors = Table(
    'project_subcontractors',
    Base.metadata,
    Column('project_id', String, ForeignKey('projects.id'), primary_key=True),
    Column('subcontractor_id', String, ForeignKey('subcontractors.id'), primary_key=True)
)


class UserORM(Base):
    """User model with authentication fields."""
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin' or 'foreman'
    email = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    asset_movements = relationship("AssetHistoryORM", back_populates="moved_by_user")


class ProjectORM(Base):
    """Project model with relationships to assets and subcontractors."""
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    assets = relationship("AssetORM", back_populates="project")
    asset_history = relationship("AssetHistoryORM", back_populates="project")
    subcontractors = relationship(
        "SubcontractorORM",
        secondary=project_subcontractors,
        back_populates="projects"
    )


class AssetORM(Base):
    """Asset model with project relationship."""
    __tablename__ = "assets"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("ProjectORM", back_populates="assets")
    history = relationship("AssetHistoryORM", back_populates="asset")
    
    # Legacy relationship for backward compatibility
    place_id = Column(String, ForeignKey("places.id"), nullable=True)
    place = relationship("PlaceORM", back_populates="assets")


class SubcontractorORM(Base):
    """Subcontractor model."""
    __tablename__ = "subcontractors"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    documents = relationship("ComplianceDocumentORM", back_populates="subcontractor")
    projects = relationship(
        "ProjectORM",
        secondary=project_subcontractors,
        back_populates="subcontractors"
    )


class ComplianceDocumentORM(Base):
    """Compliance document model with file path and expiry date."""
    __tablename__ = "compliance_documents"

    id = Column(String, primary_key=True)
    subcontractor_id = Column(String, ForeignKey("subcontractors.id"), nullable=False)
    document_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    subcontractor = relationship("SubcontractorORM", back_populates="documents")


class AssetHistoryORM(Base):
    """Asset history model for tracking movements."""
    __tablename__ = "asset_history"

    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    moved_at = Column(DateTime, server_default=func.now())
    moved_by = Column(String, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    asset = relationship("AssetORM", back_populates="history")
    project = relationship("ProjectORM", back_populates="asset_history")
    moved_by_user = relationship("UserORM", back_populates="asset_movements")


class PlaceORM(Base):
    """Legacy Place model for backward compatibility."""
    __tablename__ = "places"

    id = Column(String, primary_key=True)    
    name = Column(String)
    location = Column(String)
    assets = relationship("AssetORM", back_populates="place")
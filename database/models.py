from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class AssetORM(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    place_id = Column(String, ForeignKey("places.id"), nullable=True)
    place = relationship("PlaceORM", back_populates="assets")

class PlaceORM(Base):
    __tablename__ = "places"

    id = Column(String, primary_key=True)    
    name = Column(String)
    location = Column(String)
    assets = relationship("AssetORM", back_populates="place")
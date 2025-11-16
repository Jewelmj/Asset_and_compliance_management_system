from sqlalchemy import Column, String
from database.db import Base

class AssetORM(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)


class PlaceORM(Base):
    __tablename__ = "places"

    id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(String)
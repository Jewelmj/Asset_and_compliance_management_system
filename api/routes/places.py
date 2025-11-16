from flask import Blueprint, request
from mappers.place_mapper import PlaceMapper
from models.place import Place
from models.place_metadata import PlaceMetadata
from models.place_history import PlaceHistory
from database.db import SessionLocal

places_bp = Blueprint("places", __name__)

@places_bp.post("/")
def create_place():
    data = request.json
    name = data.get("name")
    location = data.get("location")

    domain_place = Place(
        name=name,
        location=location,
        metadata=PlaceMetadata(),
        history=PlaceHistory()
    )

    place_orm = PlaceMapper.to_orm(domain_place)

    db = SessionLocal()
    db.add(place_orm)
    db.commit()

    return {
        "place_id": domain_place.place_id,
        "name": domain_place.name,
        "location": domain_place.location,
    }, 201

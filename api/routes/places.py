from flask import Blueprint, request
from database.db import SessionLocal
from database.models import PlaceORM
import uuid

places_bp = Blueprint("places", __name__)

@places_bp.post("/")
def create_place():
    data = request.json
    name = data.get("name")
    location = data.get("location")

    place_id = str(uuid.uuid4())
    db = SessionLocal()

    place = PlaceORM(id=place_id, name=name, location=location)

    db.add(place)
    db.commit()

    return {
        "place_id": place.id,
        "name": place.name,
        "location": place.location,
    }, 201


@places_bp.get("/")
def list_places():
    db = SessionLocal()
    places = db.query(PlaceORM).all()

    return {
        "places": [
            {
                "place_id": p.id,
                "name": p.name,
                "location": p.location,
                "asset_count": 0,   
                "people_count": 0,
            }
            for p in places
        ]
    }
from flask import Blueprint, request
from services.place_service import PlaceService

places_bp = Blueprint("places", __name__)

PLACES_DB = {}
place_service = PlaceService()

@places_bp.post("/")
def create_place():
    data = request.json
    name = data.get("name")
    location = data.get("location")

    place = place_service.create_place(name, location)

    PLACES_DB[place.place_id] = place

    return {
        "place_id": place.place_id,
        "name": place.name,
        "location": place.location
    }, 201

@places_bp.get("/")
def list_places():
    return {
        "places": [
            {
                "place_id": p.place_id,
                "name": p.name,
                "location": p.location,
                "asset_count": p.assets.count(),
                "people_count": p.people.count()
            }
            for p in PLACES_DB.values()
        ]
    }
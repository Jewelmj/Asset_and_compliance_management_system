from models.place import Place
from database.models import PlaceORM

class PlaceMapper:

    @staticmethod
    def to_orm(domain_place: Place) -> PlaceORM:
        return PlaceORM(
            id=domain_place.place_id,
            name=domain_place.name,
            location=domain_place.location
        )

    @staticmethod
    def to_domain(place_orm: PlaceORM) -> Place:
        return Place(
            name=place_orm.name,
            location=place_orm.location,
            metadata=None,
            history=None
        )

from sqlalchemy import func
from src.extensions import db
from src.models.location import Location


def list_locations(offset, limit):
    count = db.session.query(func.count(Location.id)).scalar()
    locations = Location.query.order_by(
        Location.update_date).offset(offset).limit(limit).all()

    return {"count": count, "arr": locations}


def create_location(author_id, **kwargs):
    country = kwargs.get('country', None)
    city = kwargs.get('city', None)
    address = kwargs.get('address')
    creation_date = kwargs.get('creation_date', None)
    update_date = kwargs.get('update_date', None)

    new_location = Location(
        address=address,
        author_id=author_id,
        country=country,
        city=city,
        creation_date=creation_date,
        update_date=update_date
    )

    db.session.add(new_location)
    db.session.commit()

    return new_location.json()


def update_location(id, **kwargs):
    location = Location.query.get(id)
    if location is None:
        raise Exception(f'Location with id:{id} was not found!')

    location.country = kwargs.get('country', location.country)
    location.city = kwargs.get('city', location.city)
    location.address = kwargs.get('address', location.address)
    location.creation_date = kwargs.get(
        'creation_date', location.creation_date)
    location.update_date = kwargs.get('update_date', location.update_date)

    db.session.commit()

    return location.json()


def delete_location(id):
    location = Location.query.get(id)
    if location is None:
        raise Exception(f'Location with id:{id} was not found!')

    db.session.delete(location)
    db.session.commit()

    return

from sqlalchemy import func
from src.extensions import db
from src.models.provider import Provider


def get_providers(offset, limit):
    count = db.session.query(func.count(Provider.id)).scalar()
    providers = Provider.query.order_by(
        Provider.update_date).offset(offset).limit(limit).all()
    return {"count": count, "arr": providers}


def create_provider(authord_id, **kwargs):
    name = kwargs['name']
    email = kwargs['email']
    tel = kwargs['tel']
    contact_person = kwargs['contact_person']
    currency_id = kwargs['currency_id']
    location_id = kwargs['location_id']
    website = kwargs.get('website') or None
    creation_date = kwargs.get('creation_date') or None
    update_date = kwargs.get('update_date') or None

    new_provider = Provider(
        name=name,
        email=email,
        tel=tel,
        contact_person=contact_person,
        currency_id=currency_id,
        location_id=location_id,
        website=website,
        creation_date=creation_date,
        update_date=update_date,
        author_id=authord_id
    )

    db.session.add(new_provider)
    db.session.commit()

    return new_provider

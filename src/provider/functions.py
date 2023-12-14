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


def update_provider(
        id,
        **kwargs
):
    provider = Provider.query.get(id)
    if provider is None:
        raise Exception(f'Provider with id {id} was not found!')

    provider.name = kwargs.get('name', provider.name)
    provider.email = kwargs.get('email', provider.email)
    provider.tel = kwargs.get('tel', provider.tel)
    provider.contact_person = kwargs.get(
        'contact_person', provider.contact_person)
    provider.currency_id = kwargs.get('currency_id', provider.currency_id)
    provider.location_id = kwargs.get('location_id', provider.location_id)
    provider.website = kwargs.get('website', provider.website)
    provider.creation_date = kwargs.get(
        'creation_date', provider.creation_date)
    provider.update_date = kwargs.get('update_date', provider.update_date)

    db.session.commit()

    return provider.json()


def delete_provider(id):
    provider = Provider.query.get(id)
    if provider is None:
        raise Exception(f'Provider with id:{id} was not found!')

    db.session.delete(provider)
    db.session.commit()

    return

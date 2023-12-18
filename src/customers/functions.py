from sqlalchemy import func
from src.models.customer import Customer
from src.extensions import db


def list_customers(limit, offset):
    count = db.session.query(func.count(Customer.id)).scalar()
    customer_list = Customer.query.order_by(
        Customer.update_date).limit(limit).offset(offset).all()
    return {"count": count, "arr": customer_list}


def create_customer(author_id, **kwargs):
    name = kwargs['name']
    email = kwargs['email']
    tel = kwargs['tel']
    contact_person = kwargs['contact_person']
    currency_id = kwargs['currency_id']
    location_id = kwargs['location_id']
    creation_date = kwargs.get('creation_date', None)
    update_date = kwargs.get('update_date', None)

    new_customer = Customer(
        name=name,
        email=email,
        tel=tel,
        contact_person=contact_person,
        currency_id=currency_id,
        location_id=location_id,
        creation_date=creation_date,
        update_date=update_date,
        author_id=author_id
    )

    db.session.add(new_customer)
    db.session.commit()

    return new_customer.json()


def update_customer(id, **kwargs):
    customer = Customer.query.get(id)
    if customer is None:
        raise Exception(f'Customer with id:{id} was not found!')

    customer.name = kwargs.get('name', customer.name)
    customer.email = kwargs.get('email', customer.email)
    customer.tel = kwargs.get('tel', customer.tel)
    customer.contact_person = kwargs.get(
        'contact_person', customer.contact_person)
    customer.currency_id = kwargs.get('currency_id', customer.currency_id)
    customer.location_id = kwargs.get('location_id', customer.location_id)
    customer.creation_date = kwargs.get(
        'creation_date', customer.creation_date)
    customer.update_date = kwargs.get('update_date', customer.update_date)

    db.session.commit()

    return customer.json()


def delete_customer(id):
    customer = Customer.query.get(id)
    if customer is None:
        raise Exception(f'Customer with id:{id} was not found!')

    db.session.delete(customer)
    db.session.commit()
    return

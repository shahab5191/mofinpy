from marshmallow.utils import is_instance_or_subclass
from sqlalchemy import func
from src.extensions import db
from src.models.history import History
from src.utils.pagination import pagination_return_format


class CRUD():
    def __init__(self, model, create_schema, update_schema, name):
        if not is_instance_or_subclass(model, db.Model):
            raise Exception('model is not instance of db.Model')
        if not isinstance(name, str):
            raise Exception('name should be string')
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.name = name

    def get(self, id):
        item = self.model.query.get(id)
        if item is None:
            return {"err": f'{self.name} with id:{id} was not found!'}, 404

        return {self.name: item.json()}, 200

    def get_all(self, args):
        count = db.session.query(func.count(
            getattr(self.model, 'id'))).scalar()
        limit = args.get('limit', 10)
        offset = args.get('offset', 0)
        item_list = self.model.query.order_by(
            getattr(self.model, 'update_date')).limit(limit).offset(offset).all()

        return pagination_return_format(
            count=count,
            items=item_list,
            offset=offset
        )

    def create(self, user_id, data):
        if data is None:
            return {"err": "You should provide required data"}, 400
        errors = self.create_schema.validate(data)
        if errors:
            print('[crud_create]', errors)
            return {"err": errors}, 400
        new_item = self.model(**data)
        db.session.add(new_item)
        db.session.commit()
        new_history = History(user_id=user_id,
                              model_name=self.model.__tablename__,
                              record_id=new_item.id,
                              action="Create",
                              )
        db.session.add(new_history)
        db.session.commit()
        return {self.name: new_item.json()}, 201

    def update(self, id, user_id, data):
        if data is None:
            return {"err": "You should provide atleast 1 field to update"}, 400

        errors = self.update_schema.validate(data)
        if errors:
            return {"err": errors}, 400

        item = self.model.query.get(id)
        if item is None:
            return {"err": f'{self.name} with id:{id} was not found!'}

        # here we iterate throw all attributes of model and
        # change its value if it is available in data
        for attr in dir(self.model):
            if not attr.startswith('__') and not callable(getattr(self.model, attr)):
                setattr(item, attr, data.get(attr, getattr(item, attr)))

        new_history = History(user_id=user_id,
                              model_name=self.model.__tablename__,
                              record_id=item.id,
                              action="Update",
                              changes=str(data)
                              )
        db.session.add(new_history)
        db.session.commit()
        return {"item": item.json()}

    def delete(self, id, user_id):
        item = self.model.query.get(id)
        if item is None:
            return {"err": f'{self.name} with id:{id} was not found!'}, 404
        db.session.delete(item)
        new_history = History(user_id=user_id,
                              model_name=self.model.__tablename__,
                              record_id=item.id,
                              action="Delete",
                              )
        db.session.add(new_history)
        db.session.commit()

        return {
            "msg": f'{self.name} with id:{id} was deleted successfully!'
        }, 201

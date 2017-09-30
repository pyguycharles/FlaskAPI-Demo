import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
            type=float,
            required=True,
            help='this field cannot be left blank!'
    )

    parser.add_argument('store_id',
            type=int,
            required=True,
            help='every item needs a store id'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'Item does not exist'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exist'}, 400

        data = Item.parser.parse_args()
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except Exception as e:
            return {'message': 'An error occured updating this item | %s' % e}, 500
        return {'name': name, 'price': data['price']}


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db() 
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

     
class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)

        items = {'items': [item.json() for item in ItemModel.query.all()]}
        # items = {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

        # items = [dict(zip([key[0] for key in cursor.description], row)) for row in result]

        return items




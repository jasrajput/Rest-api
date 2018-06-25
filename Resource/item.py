import sqlite3
from flask import Flask
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
# from security import authenticate, identity


class Item(Resource): # Below parser now is belong to class item.now we can call it with dot. from anywhere.
    parser = reqparse.RequestParser() # it initialize as new obj. which we use to parse the req.we run req through it.
    parser.add_argument('price',
               type=float,
               required=True,
               help="This field can't be left blank"
        )                                            # what arguments matches we define in the parser and make sure the price argument is there..the req terminate when price field was not there.. 
    
    @jwt_required() # it need jwt token to get authorised..we can put it on any place like post , delete etc
    def get(self, name):
       item = ItemModel.find_by_name(name)
       if item:
           return item.json()
       return {"message": "item not found"},404
        # for item in items:0
        #     # if item['name']==name:
        #     #     return item
        #             or 
        # item = next(filter(lambda x: x['name'] == name, items), None) # if next fun doesn't find any item, it returns none 
        # return {'item': item}, 200 if item else 204

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}'already exists.".format(name)}, 404

        data = Item.parser.parse_args()  # load data.

        item = ItemModel(name, data['price'])
        # print(name)
        # print(data['price'])
        item.insert()
        return item.json(), 201


    def delete(self, name):
        connection = sqlite3.connect('data.db') 
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()
        return {'message': 'item deleted'}
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))#our item list is a list result of filtering on lambda where name is not equal to the name,that was passed in.


    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured inserting the item."},500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occured inserting the item."},500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        
        connection.close()
       
        return {"items": items}        

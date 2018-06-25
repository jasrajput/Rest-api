from flask import Flask
from flask_restful import Api #reqparse- designed to provide simple and uniform access to any variable 
from flask_jwt import JWT
from security import authenticate, identity
from resources.item import Item, ItemList

from resources.user import UserRegister

app =  Flask(__name__)
app.secret_key = 'jose'
api = Api(app)


jwt = JWT(app, authenticate, identity) 
# jwt creates a new endpoint(/auth).when we call auth
# we send it username and password and then jwt extens. takes the username and password and 
# send it to the authenticate function

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>') #http:127.0.0.1.5000/item/item_name
api.add_resource(UserRegister, '/register')
if __name__ == '__main__':
    app.run(port=5000, debug=True)


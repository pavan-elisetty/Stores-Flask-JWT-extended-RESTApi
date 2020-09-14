from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'Store not found'} , 404


    def post(self , name):
        if StoreModel.find_by_name(name):
            return {'message':'store already there with that name'} , 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occured while creating the user'},500
        return store.json() , 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':'store deleted'}

class StoreList(Resource):
    def get(self):
        #return {'stores':[store.json() for store in StoreModel.query.all()]}
        return {'stores': [x.json() for x in StoreModel.find_all()]}
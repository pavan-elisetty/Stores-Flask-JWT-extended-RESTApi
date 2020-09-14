from flask_restful import Resource , reqparse
from flask_jwt_extended import(
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
#RESOURCES ARE SUMTNG WHERE ONLY THE CLIENTS INTERACT WITH LIKE API ENDPOINTS
from models.item import ItemModel




class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,  # making price mandatory
                        help='This field cannot be left blank'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,  # making price mandatory
                        help='Every item needs a store id'
                        )

    #data = _user_parser.parse_args()
    @jwt_required
    def get(self , name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message':'item not found'} , 404

#while using flask restful we dont need to do jsonify as it already does that

    @fresh_jwt_required
    def post(self , name):

        if ItemModel.find_by_name(name):
            return{'message':'An item with name {} already existed!'.format(name)} , 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) #returning ItemModel object
        #data['price'],data['store_id']
        try:
            item.save_to_db()
        except:
            return {"message":"an error occured inserting an item"} , 500 #internal server error



        return item.json() , 201 #201 code for creating

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin privelage required'},401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}


    def put(self , name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item=ItemModel(name,**data)
        item.save_to_db()
        return item.json()




class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()#returns user id saved in jwt
        items = [x.json() for x in ItemModel.find_all()] #returns item in json
        if user_id:
            return {'items':items},200
        return {
            'items':[item['name'] for item in items], #returns only some data i.e., names
            'message':'More data available if the user is logged in'
        },200
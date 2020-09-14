from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_refresh_token,
    create_access_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from flask_restful import Resource , reqparse
from models.user import UserModel
from blacklist import BLACKLIST
#getting data from json payload
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="this field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="this field cannot be blank."
                          )
#_user_parser for getting inputs





class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'A user with that username already exists'}


        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user created sucessfully"} , 201 #201 for created

class User(Resource):
    @classmethod
    def get(cls,user_id):
        user=UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User not found'},404
        return user.json()


    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'user not found'},404
        user.delete_from_db()
        return {'message':'User deleted'},200


class UserLogin(Resource):


    @classmethod
    def post(cls):

        #get data from _user_parser
        data = _user_parser.parse_args()

        #find user in database
        user = UserModel.find_by_username(data['username'])

        #just as authenticate function
        #check password
        if user and safe_str_cmp(user.password , data['password']):
            #this is similar to what the identity function used to do
            access_token = create_access_token(identity = user.id , fresh = True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        return {'message':'Invalid credentials'},401
        #create access token and refresh token
        #refresh item


class UserLogout(Resource):
    @jwt_required
    def post(self): #blacklisting their current jwt so as to achieve logout
        jti =  get_raw_jwt()['jti'] #jti is JWT ID , a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message':'successfully logged out'},200



class TokenRefresh(Resource):
    @jwt_refresh_token_required #we need to have a refresh token or it returns error
    def post(self):
        current_user =get_jwt_identity() #it works with both access and refresh tokens
        new_token = create_access_token(identity=current_user , fresh=False)
        return {'access_token':new_token},200

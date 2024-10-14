from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(15), nullable=False)
  password = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)

User_put_args=reqparse.RequestParser()
User_put_args.add_argument('user_id', type=int, help='The User-id was not found', required=True)
User_put_args.add_argument('name', type=str, help='The Name was not found', required=True)
User_put_args.add_argument('password', type=str, help='The Password was not found', required=True)
User_put_args.add_argument('email', type=str, help='The Email was not found', required=True)

resource_fields= {
  'user_id':fields.Integer,
  'name':fields.String,
  'password':fields.String,
  'email':fields.String
}
class User(Resource):
  @marshal_with(resource_fields)
  def get(self, user_id): #to look for the information of a specific user
    result_user_id = UserModel.query.filter_by(user_id=user_id).first()
    if not result_user_id:
      abort(404, message='Could not give information for the requested user.')
    return result_user_id

  @marshal_with(resource_fields)
  def put(self, user_id): #register
    args =User_put_args.parse_args()
    results = UserModel.query.filter_by(user_id=user_id).first()
    if results:
      abort(409, message='error')
    user = UserModel(user_id=user_id,name=args['name'], email=args['email'], password=args['password'] )
    db.session.add(user)
    db.session.commit()
    return user, 201

api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)

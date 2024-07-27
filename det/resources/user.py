from flask_restful import Resource, reqparse
from models import User, db
from schemas.user import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email is required')
        parser.add_argument('name', required=True, help='Name is required')
        parser.add_argument('mobile', required=True, help='Mobile number is required')
        args = parser.parse_args()

        user = User(email=args['email'], name=args['name'], mobile=args['mobile'])
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user)

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user)

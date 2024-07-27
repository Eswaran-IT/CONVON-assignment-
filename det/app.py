from flask import Flask
from flask_restful import Api
from models import db
from resources.user import UserResource
from resources.expense import ExpenseResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(ExpenseResource, '/expenses', '/expenses/<int:user_id>')

@app.route('/')
def home():
    return 'API is running', 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

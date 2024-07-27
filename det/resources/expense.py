from flask_restful import Resource, reqparse
from models import Expense, db
from schemas.expense import ExpenseSchema
from utils.calculations import calculate_equal_split, calculate_exact_split, calculate_percentage_split

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

class ExpenseResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True, help='Description is required')
        parser.add_argument('amount', type=float, required=True, help='Amount is required')
        parser.add_argument('date', required=True, help='Date is required')
        parser.add_argument('split_method', required=True, help='Split method is required')
        parser.add_argument('splits', type=dict, action='append', required=True, help='Splits information is required')
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        args = parser.parse_args()

        expense = Expense(
            description=args['description'],
            amount=args['amount'],
            date=args['date'],
            split_method=args['split_method'],
            splits=args['splits'],
            user_id=args['user_id']
        )

        # Calculate splits based on method
        if args['split_method'] == 'EQUAL':
            participants = len(args['splits'])
            split_amount = calculate_equal_split(args['amount'], participants)
            for split in args['splits']:
                split['amount'] = split_amount
        elif args['split_method'] == 'EXACT':
            splits = calculate_exact_split(args['splits'])
        elif args['split_method'] == 'PERCENTAGE':
            percentages = [split['percentage'] for split in args['splits']]
            amounts = calculate_percentage_split(args['amount'], percentages)
            for split, amount in zip(args['splits'], amounts):
                split['amount'] = amount

        db.session.add(expense)
        db.session.commit()
        return expense_schema.jsonify(expense)

    def get(self, user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()
        return expenses_schema.jsonify(expenses)

from models import Expense
from schemas import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ExpenseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Expense
        load_instance = True


from utils.marsh_util import marsh
from models.transaction import Transaction

class TransactionSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True 
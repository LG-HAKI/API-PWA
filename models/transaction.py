from utils.db_util import db
from sqlalchemy.exc import IntegrityError
from datetime import date

class Transaction(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(scale=2), nullable=False)
    transaction_dt = db.Column(db.Date, default=date.today())

    def __init__(self, buyer_id, seller_id, item_id, value):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.item_id = item_id
        self.value = value


    @classmethod
    def get_transaction_by_buyerid(cls, id):
        return cls.query.filter_by(buyer_id = id).all()
    
    def add_transaction(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback() 
            raise Exception(str(e.orig))
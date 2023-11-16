from utils.db_util import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), nullable=False)
    author = db.Column(db.String(140), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    edition_dt = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.String(60), nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)


    def __init__(self, title, author, category_id, price, description, edition_dt, freq, seller_id):
            self.title = title
            self.author = author
            self.category_id = category_id
            self.price = price
            self.description = description
            self.edition_dt = datetime.strptime(edition_dt, '%Y-%m-%d').date()
            self.seller_id = seller_id

            if freq not in ["diario", "semanal", "quinzenal", "mensal", "semestral", "anual"]:
                raise ValueError(f"Valor '{freq}' não permitido para a coluna 'frequencia'")
            
            self.frequency = freq
        
    @classmethod
    def get_items(cls):
        return cls.query.all()
    
    @classmethod
    def get_item_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
    
    @classmethod
    def get_item_by_id_in_stock(cls, id):
        return cls.query.filter_by(id = id, in_stock = True).first()
    
    def add_item(self):
        self.save_to_db()
    
    def update_item(self, price, freq):
        try:
            self.price = price 
            if freq not in ["diario", "semanal", "quinzenal", "mensal", "semestral", "anual"]:
                raise ValueError(f"Valor '{freq}' não permitido para a coluna 'frequencia'")
            self.frequency = freq
            self.save_to_db()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback() 
            raise Exception(str(e.orig))
        
    def delete_from_db(self):
        try:
            self.in_stock = not self.in_stock
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

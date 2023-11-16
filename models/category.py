from utils.db_util import db
from sqlalchemy.exc import IntegrityError

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def get_categories(cls):
        return cls.query.filter_by(active = True).all()
    
    @classmethod
    def get_category_by_id(cls, id):
        return cls.query.filter_by(id = id, active = True).first()

    
    def add_category(self, name):
        cat = self.query.filter_by(name=name).first()

        if cat:
            if not cat.active:
                cat.active = not cat.active
                cat.save_to_db()
            else:
                raise ValueError("A categoria já existe")
        else:
            self.save_to_db()
    
    def update_category(self, name, description):
        self.name = name 
        self.description = description
        try:
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
            self.active = not self.active
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))    
        
    

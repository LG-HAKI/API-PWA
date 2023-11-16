from utils.db_util import db
from sqlalchemy.exc import IntegrityError
from datetime import date


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(140), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    start_dt = db.Column(db.Date, default=date.today())
    expertise = db.Column(db.String(40), nullable=True)

    def __init__(self, name, email, password, user_type, expertise=None):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.expertise = expertise


    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id, active=True).first()
    
    @classmethod
    def get_user_info(cls, email):
        return cls.query.with_entities(cls.id, cls.password, cls.user_type).filter_by(email=email, active=True).first()
    
    @classmethod
    def get_users(cls):
        return cls.query.filter_by(active=True).all()
    
    @classmethod
    def get_count_users_type(cls):
        comp = cls.query.filter_by(user_type="comprador", active=True).count()
        vend = cls.query.filter_by(user_type="vendedor", active=True).count()
        admin = cls.query.filter_by(user_type="admin", active=True).count()
        inat = cls.query.filter_by(active=False).count()

        return comp, vend, admin, inat

    
    def user_update(self, name, password):
        self.name = name 
        self.password = password
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
        self.active = not self.active
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))



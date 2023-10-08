from utils.marsh_util import marsh
from models.user import User

class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
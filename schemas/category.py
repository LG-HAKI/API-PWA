from utils.marsh_util import marsh
from models.category import Category

class CategorySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True 
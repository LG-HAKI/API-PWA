from utils.marsh_util import marsh
from models.item import Item

class ItemSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True 
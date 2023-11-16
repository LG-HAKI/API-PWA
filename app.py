from flask import Flask
from flask_jwt_extended import JWTManager
from controllers.user_controller import user_routes
from controllers.admin_controller import admin_routes
from controllers.category_controller import category_routes
from controllers.item_controller import item_routes
from controllers.transaction_controller import transaction_routes

from utils.db_util import db
from utils.marsh_util import marsh
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "@n3P!3c3"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager()

user_routes(app)
admin_routes(app)
item_routes(app)
category_routes(app)
transaction_routes(app)


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    marsh.init_app(app)
    jwt.init_app(app)
    app.run(debug=True)

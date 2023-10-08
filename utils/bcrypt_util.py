from flask_bcrypt import Bcrypt
from utils.validation_util import validate_password

bcrypt = Bcrypt()

def generate_password_hash(password):
    if validate_password(password):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return password_hash
    else:
        return None

def check_password(stored_password_hash, password_to_check):
    return bcrypt.check_password_hash(stored_password_hash, password_to_check)
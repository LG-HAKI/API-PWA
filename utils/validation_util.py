import re

def validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?!.*_)\w{6,}$"
    
    if re.match(pattern, password):
        return True
    else:
        return False

def validate_email(email):
    pattern = r"^[a-zA-Z]+[a-zA-Z0-9_.+-]+@(gmail\.com|outlook\.com|hotmail\.com)$"

    if re.match(pattern, email):
        return True
    else:
        return False